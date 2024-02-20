{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/22.05.tar.gz") {} }:
with pkgs;
let
    celluloid2 = python310Packages.buildPythonPackage rec {
    pname = "celluloid";
    version = "0.2.0";
    src = python310Packages.fetchPypi {
      inherit pname version;
      sha256 =
        "568b1512c4a97483759e9436c3f3e5dc5566da350179aa1872992ec8d82706e1";
    };
    propagatedBuildInputs = [ python310Packages.matplotlib ];
    };
    pythonBundle = python310.withPackages (ps: with ps; [ numpy matplotlib mypy celluloid2 ]);
in
mkShell {
    buildInputs = [ pythonBundle ];
}
