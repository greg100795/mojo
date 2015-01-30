#!/usr/bin/env python
# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import argparse
import os
import subprocess
import sys
import tempfile
import time
import zipfile

import mopy.gn as gn
from mopy.config import Config
from mopy.paths import Paths
from mopy.version import Version

def upload(config, dry_run, verbose):
  paths = Paths(config)

  sys.path.insert(0, os.path.join(paths.src_root, "tools"))
  # pylint: disable=F0401
  import find_depot_tools

  depot_tools_path = find_depot_tools.add_depot_tools_to_path()
  gsutil_exe = os.path.join(depot_tools_path, "third_party", "gsutil", "gsutil")

  zipfile_name = "%s-%s" % (config.target_os, config.target_arch)
  dest = "gs://mojo/shell/" + Version().version + "/" + zipfile_name + ".zip"

  with tempfile.NamedTemporaryFile() as zip_file:
    with zipfile.ZipFile(zip_file, 'w') as z:
      shell_path = paths.target_mojo_shell_path
      with open(shell_path) as shell_binary:
        shell_filename = os.path.basename(shell_path)
        zipinfo = zipfile.ZipInfo(shell_filename)
        zipinfo.external_attr = 0777 << 16L
        compress_type = zipfile.ZIP_DEFLATED
        if config.target_os == Config.OS_ANDROID:
          # The APK is already compressed.
          compress_type = zipfile.ZIP_STORED
        zipinfo.compress_type = compress_type
        zipinfo.date_time = time.gmtime(os.path.getmtime(shell_path))
        if verbose:
          print "zipping %s" % shell_path
        z.writestr(zipinfo, shell_binary.read())
    if dry_run:
      print str([gsutil_exe, "cp", zip_file.name, dest])
    else:
      subprocess.check_call([gsutil_exe, "cp", zip_file.name, dest])

def main():
  parser = argparse.ArgumentParser(description="Upload mojo_shell binary to "+
      "google storage (by default on Linux, but this can be changed via options"
      ".")
  parser.add_argument("-n", "--dry_run", help="Dry run, do not actually "+
      "upload", action="store_true")
  parser.add_argument("-v", "--verbose", help="Verbose mode",
      action="store_true")
  parser.add_argument("--android",
                      action="store_true",
                      help="Upload the shell for Android")
  args = parser.parse_args()

  target_os = Config.OS_LINUX
  if args.android:
    target_os = Config.OS_ANDROID
  config = Config(target_os=target_os, is_debug=False)
  upload(config, args.dry_run, args.verbose)
  return 0

if __name__ == "__main__":
  sys.exit(main())
