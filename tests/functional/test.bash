#!/usr/bin/env bash

#  Copyright (c) 2015-2016 Cisco Systems
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#  THE SOFTWARE.

# NOTE(retr0h): A very basic functional test.  Will expand upon this.

set -e

export FUNCTIONAL_TEST_BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
export TMP_DIR=$(mktemp -d /tmp/tmp.XXXXXXXXXX)
ANSIBLE_MAJOR_VERSION=$(ansible --version|head -1|awk '{print $NF}'|cut -d\. -f1)

source ${VIRTUAL_ENV}/bin/activate

if [ ${ANSIBLE_MAJOR_VERSION} != 1 ]; then
	echo "### Docker driver"
	source ${FUNCTIONAL_TEST_BASE_DIR}/test_docker_init.bash
fi

echo "### Vagrant driver"
source ${FUNCTIONAL_TEST_BASE_DIR}/test_vagrant_test.bash
