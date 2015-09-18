class EnlightnsCli < Formula
  version "0.0.23"
  desc "Enlightns.com Command Line Interface"
  homepage "https://enlightns.com/"
  head "https://github.com/EnlightNS/enlightns-cli.git"
  url "https://github.com/EnlightNS/enlightns-cli/archive/0.0.23.tar.gz"
  sha256 "43fe7640aa53f6d854c2c7f6ab2601459191d682e7172c309f6aa6d906aa927a"

  depends_on :python
  depends_on "pkg-config" => :build
  depends_on "libffi"

  resource "click" do
    url "https://pypi.python.org/packages/2.7/c/click/click-5.1-py2.py3-none-any.whl"
    sha1 "6011aa9dc82e7dc33cf10daea79603b618811218"
  end

  resource "idna" do
    url "https://pypi.python.org/packages/2.7/i/idna/idna-2.0-py2.py3-none-any.whl"
    sha1 "63cc74d3976b9f8dfe95982e9f56b2870e286b48"
  end

  resource "ipaddress" do
    url "https://pypi.python.org/packages/2.7/i/ipaddress/ipaddress-1.0.14-py27-none-any.whl"
    sha1 "230b1064dab227535581596cb8ffa3c67aba877a"
  end

  resource "py" do
    url "https://pypi.python.org/packages/2.7/p/py/py-1.4.30-py2.py3-none-any.whl"
    sha1 "cffb29158ae1954b57a38a29baea9951d5a7ac78"
  end

  resource "pytest" do
    url "https://pypi.python.org/packages/2.7/p/pytest/pytest-2.7.2-py2.py3-none-any.whl"
    sha1 "cf6523af37dc589c39f87d8f1f70b36aeab7d20e"
  end

  resource "requests" do
    url "https://pypi.python.org/packages/2.7/r/requests/requests-2.7.0-py2.py3-none-any.whl"
    sha1 "fc698280c2c29d442187d3a80a2b41c18739de3b"
  end

  resource "six" do
    url "https://pypi.python.org/packages/3.3/s/six/six-1.9.0-py2.py3-none-any.whl"
    sha1 "87c40e62532048e19146e2c61f76e359a2be6413"
  end

  resource "python-dateutil" do
    url "https://pypi.python.org/packages/any/p/python-dateutil/python_dateutil-2.4.2-py2.py3-none-any.whl"
    sha1 "92219a524cb3e24606b064b98deb6a9ad437e0a3"
  end

  resource "cryptography" do
    url "https://pypi.python.org/packages/cp27/c/cryptography/cryptography-1.0.1-cp27-none-macosx_10_10_x86_64.whl"
    sha1 "2c968db2fa5d0607c6ba5b99ab22edf9e7b1a987"
  end

  resource "pyOpenSSL" do
    url "https://pypi.python.org/packages/py2.py3/p/pyOpenSSL/pyOpenSSL-0.15.1-py2.py3-none-any.whl"
    sha1 "391c319491cc4a8a29a3e9c332f36e5915c81d90"
  end

  resource "IPy" do
    url "https://pypi.python.org/packages/source/I/IPy/IPy-0.83.tar.gz"
    sha1 "0836e6788479b6507bccac1f9607c646d9c2562c"
  end

  resource "cffi" do
    url "https://pypi.python.org/packages/source/c/cffi/cffi-1.2.1.tar.gz"
    sha1 "f7ed014ff1602a8e81073f5356b4cafbc3f5dce1"
  end

  resource "colorama" do
    url "https://pypi.python.org/packages/source/c/colorama/colorama-0.3.3.tar.gz"
    sha1 "a8ee91adf4644bbdccfc73ead88f4cd0df7e3552"
  end

  resource "dnspython" do
    url "https://pypi.python.org/packages/source/d/dnspython/dnspython-1.12.0.zip"
    sha1 "e1d81af983d37c5478fe04694b78014b46210c5e"
  end

  resource "enum34" do
    url "https://pypi.python.org/packages/source/e/enum34/enum34-1.0.4.tar.gz"
    sha1 "10b77f1db47e54abbc4ce6f61df542590b9ad972"
  end

  resource "ndg-httpsclient" do
    url "https://pypi.python.org/packages/source/n/ndg-httpsclient/ndg_httpsclient-0.4.0.tar.gz"
    sha1 "82f6a1797b80a544cbfbc7f9f1df41da8463248d"
  end

  resource "netifaces" do
    url "https://pypi.python.org/packages/source/n/netifaces/netifaces-0.10.4.tar.gz"
    sha1 "c3fcd491a89c2994815053e853b005e7fc27c79a"
  end

  resource "ordereddict" do
    url "https://pypi.python.org/packages/source/o/ordereddict/ordereddict-1.1.tar.gz"
    sha1 "ab90b67dceab55a11b609d253846fa486eb980c4"
  end

  resource "pyasn1" do
    url "https://pypi.python.org/packages/source/p/pyasn1/pyasn1-0.1.8.tar.gz"
    sha1 "1fac3b68e5ae4b34ef35abf36c946d0b03a26812"
  end

  resource "pycparser" do
    url "https://pypi.python.org/packages/source/p/pycparser/pycparser-2.14.tar.gz"
    sha1 "922162bad4aa8503988035506c1c65bbf8690ba4"
  end

  resource "python-crontab" do
    url "https://pypi.python.org/packages/source/p/python-crontab/python-crontab-1.9.3.tar.gz"
    sha1 "2888b14d5630501626c56024c48f0d8268490e66"
  end

  def install
    ENV.prepend_create_path "PYTHONPATH", libexec/"vendor/lib/python2.7/site-packages"

    rs = %w[cffi click colorama cryptography dnspython enum34 idna ipaddress IPy ndg-httpsclient netifaces ordereddict py pyasn1 pycparser pyOpenSSL pytest python-crontab python-dateutil requests six]
    rs.each do |r|
      resource(r).stage do
        system "python", *Language::Python.setup_install_args(libexec)
      end
    end

    ENV.prepend_create_path "PYTHONPATH", libexec/"lib/python2.7/site-packages"
    system "python", *Language::Python.setup_install_args(libexec)
  end

  test do
    system "make", "test"
  end
end
