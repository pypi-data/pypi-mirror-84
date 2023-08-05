#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import (division, absolute_import, print_function,
                        unicode_literals)

import argparse
from contextlib import contextmanager
import ftplib
import itertools
import os
import socket
import sys
import uuid
import gevent
from gevent import pool
import timecard

__author__ = "Jose Angel Munoz <josea.munoz@gmail.com>"

try:
    import dns.resolver as resolver
except ImportError:
    resolver = None


class Data():
    chunk = "x" * 65536

    def __init__(self, size):
        self.size = size
        self.read = 0

    def __iter__(self):
        return self

    def __next__(self):
        tosend = self.size - self.read
        if tosend == 0:
            raise StopIteration

        if tosend > 65536:
            self.read += 65536
            return self.chunk
        else:
            self.read += tosend
            return self.chunk[:tosend]


class FTPBenchmark():

    def __init__(self, host, user, password, timeout, stats):
        self.hosts = host.split(",")
        self.user = user
        self.password = password
        self.timeout = timeout
        self.stats = stats
        if len(self.hosts) > 1:
            self.stats.server = timecard.MultiMetric("server")
            for h in self.hosts:
                self.stats.server[h] = timecard.Int(h)
        self.upload_files = []

        if len(self.hosts) > 1:

            def _roundrobin():
                for h in itertools.cycle(self.hosts):
                    yield h
            self._host_roundrobin = _roundrobin()

    @property
    def host(self):
        n = len(self.hosts)
        if n == 1:
            return self.hosts[0]
        else:
            h = next(self._host_roundrobin)
            self.stats.server[h] += 1
            return h

    @contextmanager
    def connect(self):
        with gevent.Timeout(self.timeout):
            ftp = ftplib.FTP(self.host)
            ftp.login(self.user, self.password)

        try:
            yield ftp
        finally:
            ftp.close()

    def upload(self, path, data):
        try:
            with self.connect() as ftp:
                self.upload_files.append(path)

                try:
                    with gevent.Timeout(self.timeout):
                        ftp.voidcmd("TYPE I")  # binary mode
                        channel = ftp.transfercmd("STOR " + path)

                    for chunk in data:
                        with gevent.Timeout(self.timeout):
                            channel.sendall(bytes(chunk, encoding='utf8'))
                            self.stats.traffic += len(chunk)

                    with gevent.Timeout(self.timeout):
                        channel.close()
                        ftp.voidresp()
                except ftplib.error_perm as e:
                    print("\n\n\rUpload Process: {0}".format(e))
                    sys.exit()
        except ConnectionRefusedError as e:
            print("\n\n\r{0}. Cannot connect to {1}".format(
                e, self.host))
            sys.exit(1)
        except (KeyboardInterrupt, gevent.Timeout):
            sys.exit()

    def download(self, path):
        try:
            with self.connect() as ftp:
                with gevent.Timeout(self.timeout):
                    ftp.voidcmd("TYPE I")  # binary mode
                    channel = ftp.transfercmd("RETR " + path)

                while True:
                    with gevent.Timeout(self.timeout):
                        chunk = channel.recv(65536)
                        if not chunk:
                            break
                        self.stats.traffic += len(chunk)

                with gevent.Timeout(self.timeout):
                    channel.close()
                    ftp.voidresp()
        except ConnectionRefusedError as e:
            print("\n\n\r{0}. Cannot connect to {1}".format(e, self.host))
            sys.exit(1)
        except (KeyboardInterrupt, gevent.Timeout):
            sys.exit()

    def clean(self):
        try:
            with self.connect() as ftp:
                for path in self.upload_files:
                    ftp.delete(path)
        except ftplib.error_perm as e:
            print("\n\n\rDownload Process: {0}".format(e))


def run_bench_login(args, stats):

    ftp = FTPBenchmark(
        args.hostname, args.username, args.password,
        int(args.timeout), stats=stats)

    print("\n\rStart login benchmark: concurrent={0} timeout={1}s maxrun={2}m\n\r".format(
        int(args.concurrent), int(args.timeout), int(args.maxrun)))

    stats.write_headers()

    def _print_stats():
        i = 0
        while True:
            i += 1
            if i == int(args.fixevery):
                stats.write_line(fix=True)
                i = 0
            else:
                stats.write_line(fix=False)
            gevent.sleep(1)

    def _check():
        stats.requests += 1
        try:
            with stats.latency():
                try:
                    with ftp.connect():
                        pass
                except (KeyboardInterrupt, gevent.Timeout):
                    sys.exit(0)
        except gevent.Timeout:
            stats.fail.timeout += 1
        except (ftplib.error_temp, ftplib.error_perm, socket.error):
            stats.fail.rejected += 1
        else:
            stats.success += 1

    gr_stats = gevent.spawn(_print_stats)
    gr_pool = pool.Pool(size=int(args.concurrent))
    try:
        with gevent.Timeout(int(args.maxrun) * 60 or None):
            while True:
                gr_pool.wait_available()
                gr_pool.spawn(_check)
    except (KeyboardInterrupt, gevent.Timeout):
        pass
    finally:
        print("\n")
        gr_stats.kill()
        gr_pool.kill()


def run_bench_upload(args, stats):

    ftp = FTPBenchmark(
        args.hostname, args.username, args.password,
        int(args.timeout), stats=stats)

    print(
        "\n\rStart upload benchmark: concurrent={0} timeout={1}s size={2}MB\n\r"
        "".format(int(args.concurrent), int(args.timeout), int(args.size)))

    stats.write_headers()

    def _print_stats():
        i = 0
        while True:
            i += 1
            if i == int(args.fixevery):
                stats.write_line(fix=True)
                i = 0
            else:
                stats.write_line(fix=False)
            gevent.sleep(1)

    def _check():
        stats.request.total += 1
        try:
            path = os.path.join(
                args.workdir, "bench_write-%s" % uuid.uuid1().hex)
            data = Data(int(args.size) * 1024 * 1024)
            with stats.uploadtime():
                ftp.upload(path, data)
        except gevent.Timeout:
            stats.request.timeout += 1
        except (ftplib.error_temp, ftplib.error_perm, socket.error):
            stats.request.rejected += 1
        else:
            stats.request.complete += 1

    gr_stats = gevent.spawn(_print_stats)
    gr_pool = pool.Pool(size=int(args.concurrent))
    try:
        with gevent.Timeout(int(args.maxrun) * 60 or None):
            while True:
                gr_pool.wait_available()
                gr_pool.spawn(_check)
    except (KeyboardInterrupt, gevent.Timeout):
        pass
    finally:
        print("\n")
        gr_stats.kill()
        gr_pool.kill()

        print("Cleanning...")
        ftp.timeout = 60
        ftp.clean()


def run_bench_download(args, stats):

    ftp = FTPBenchmark(
        args.hostname, args.username, args.password,
        int(args.timeout), stats=stats)

    print("Preparing for testing...")
    ftp.timeout = 60
    for _ in range(int(args.files)):
        path = os.path.join(
            args.workdir, "bench_read-%s" % uuid.uuid1().hex)
        data = Data(int(args.size) * 1024 * 1024)
        ftp.upload(path, data)
    ftp.timeout = int(args.timeout)
    filesiter = itertools.cycle(ftp.upload_files)

    print(
        "\n\rStart download benchmark: concurrent={0} timeout={1}s size={2}MB"
        " filecount={3}\n\r"
        "".format(
            int(args.concurrent), int(args.timeout), int(args.size),
            int(args.files)))

    stats.write_headers()

    def _print_stats():
        i = 0
        while True:
            i += 1
            if i == int(args.fixevery):
                stats.write_line(fix=True)
                i = 0
            else:
                stats.write_line(fix=False)
            gevent.sleep(1)

    def _check():
        stats.request.total += 1
        try:
            with stats.downloadtime():
                ftp.download(next(filesiter))
        except gevent.Timeout:
            stats.request.timeout += 1
        except (ftplib.error_temp, ftplib.error_perm, socket.error):
            stats.request.rejected += 1
        else:
            stats.request.complete += 1

    gr_stats = gevent.spawn(_print_stats)
    gr_pool = pool.Pool(size=int(args.concurrent))
    try:
        with gevent.Timeout(int(args.maxrun) * 60 or None):
            while True:
                gr_pool.wait_available()
                gr_pool.spawn(_check)
    except (KeyboardInterrupt, gevent.Timeout):
        pass
    finally:
        print("\n")
        gr_stats.kill()
        gr_pool.kill()
        print("Cleanning...")
        ftp.timeout = 60
        ftp.clean()


def parse_stats(args):

    stats = timecard.Timecard(args.csv)
    stats.time = timecard.AutoDateTime(show_date=False)

    if args.login:
        stats.requests = timecard.TotalAndSec("request")
        stats.success = timecard.TotalAndSec("success")
        stats.latency = timecard.Timeit("latency", limits=[1, 2, 5])
        stats.fail = timecard.MultiMetric("fails-total")
        stats.fail.timeout = timecard.Int("timeout")
        stats.fail.rejected = timecard.Int("rejected")
    elif args.upload or args.download:
        stats.request = timecard.MultiMetric("request")
        stats.request.total = timecard.Int("total")
        stats.request.complete = timecard.Int("complete")
        stats.request.timeout = timecard.Int("timeout")
        stats.request.rejected = timecard.Int("rejected")
        stats.traffic = timecard.Traffic("traffic")
        if args.upload:
            stats.uploadtime = timecard.Timeit("upload-time")
        else:
            stats.downloadtime = timecard.Timeit("download-time")

    return stats


def parse_arguments():

    fallback_args = dict(hostname='127.0.0.1',
                         default=10, maxrun=5, fixevery=5)

    parser = argparse.ArgumentParser(description='FTP Benchmark 1.1')
    parser.add_argument('--hostname',
                        '-n',
                        help='FTP host [default: 127.0.0.1:21] \
                            You can list multiple servers, separated by commas, \
                            e.g.: 10.0.0.1,10.0.0.2,10.0.0.3. Auto-detection \
                                of dns round-robin records is supported.',
                        default=fallback_args['hostname'])
    parser.add_argument('--username',
                        '-u',
                        help='FTP username')
    parser.add_argument('--password',
                        '-p',
                        help='FTP password')
    parser.add_argument('--timeout',
                        '-t',
                        help='Timeout for operation [default: 10]',
                        default=fallback_args['default'])
    parser.add_argument('--maxrun',
                        '-m',
                        help='Duration of benchmarking in minutes [default: 5]',
                        default=fallback_args['maxrun'])
    parser.add_argument('--fixevery',
                        '-x',
                        help='Recording period for stat values [default: 5]',
                        default=fallback_args['fixevery'])
    parser.add_argument('--concurrent',
                        '-c',
                        help='Concurrent operations [default: 10]',
                        default=fallback_args['default'])
    parser.add_argument('--csv',
                        '-v',
                        help='Save result to csv file')
    parser.add_argument('--workdir',
                        '-w',
                        help='Base ftp dir to store test files',
                        required='--upload' in " ".join(sys.argv) or
                        '--download' in " ".join(sys.argv))
    parser.add_argument('--size',
                        '-s',
                        help='Size of test files in MB [default: 10]',
                        default=fallback_args['default'])
    parser.add_argument('--files',
                        '-f',
                        help='Number of files generated for download test [default: 10]',
                        default=fallback_args['default'])

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--login', action='store_true')
    group.add_argument('--upload', action='store_true')
    group.add_argument('--download', action='store_true')
    return parser.parse_args()


def main():

    try:
        args = parse_arguments()
        stats = parse_stats(args)

        if resolver and "," not in args.hostname:
            try:
                hosts = []
                for x in resolver.query(args.hostname, "A"):
                    hosts.append(x.to_text())
                args.hostname = ",".join(hosts)
            except resolver.NXDOMAIN:
                pass
    except EnvironmentError as e:
        print(e.message)
    else:
        if args.login:
            run_bench_login(args, stats)
        elif args.upload:
            run_bench_upload(args, stats)
        elif args.download:
            run_bench_download(args, stats)
        else:
            sys.exit(1)


if __name__ == '__main__':
    main()
