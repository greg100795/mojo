# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Build/test configurations, which are just dictionaries. This
"defines" the schema and provides some wrappers."""


import json
import os.path
import sys


class Config(object):
  """A Config is basically just a wrapper around a dictionary that species a
  build/test configuration. The dictionary is accessible through the values
  member."""

  # Valid values for target_os (None is also valid):
  OS_ANDROID = "android"
  OS_CHROMEOS = "chromeos"
  OS_LINUX = "linux"
  OS_MAC = "mac"
  OS_WINDOWS = "windows"

  # Valid values for sanitizer (None is also valid):
  SANITIZER_ASAN = "asan"

  # Standard values for test types (test types are arbitrary strings; other
  # values are allowed).
  TEST_TYPE_DEFAULT = "default"
  TEST_TYPE_UNIT = "unit"
  TEST_TYPE_PERF = "perf"
  TEST_TYPE_INTEGRATION = "integration"

  def __init__(self, target_os=None, is_debug=True, is_clang=None,
               sanitizer=None, **kwargs):
    """Constructs a Config with key-value pairs specified via keyword arguments.
    If target_os is not specified, it will be set to the host OS."""

    assert target_os in (None, Config.OS_ANDROID, Config.OS_CHROMEOS,
                         Config.OS_LINUX, Config.OS_MAC, Config.OS_WINDOWS)
    assert isinstance(is_debug, bool)
    assert is_clang is None or isinstance(is_clang, bool)
    assert sanitizer in (None, Config.SANITIZER_ASAN)
    if "test_types" in kwargs:
      assert isinstance(kwargs["test_types"], list)

    self.values = {}
    self.values["target_os"] = (self.GetHostOS() if target_os is None else
                                target_os)
    self.values["is_debug"] = is_debug
    self.values["is_clang"] = is_clang
    self.values["sanitizer"] = sanitizer

    self.values.update(kwargs)

  @staticmethod
  def GetHostOS():
    if sys.platform == "linux2":
      return Config.OS_LINUX
    if sys.platform == "darwin":
      return Config.OS_MAC
    if sys.platform == "win32":
      return Config.OS_WINDOWS
    raise NotImplementedError("Unsupported host OS")

  # Getters for standard fields ------------------------------------------------

  @property
  def target_os(self):
    """OS of the build/test target."""
    return self.values["target_os"]

  @property
  def is_debug(self):
    """Is Debug build?"""
    return self.values["is_debug"]

  @property
  def is_clang(self):
    """Should use clang?"""
    return self.values["is_clang"]

  @property
  def sanitizer(self):
    """Sanitizer to use, if any."""
    return self.values["sanitizer"]

  @property
  def test_types(self):
    """List of test types to run."""
    return self.values.get("test_types", [Config.TEST_TYPE_DEFAULT])
