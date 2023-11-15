{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/archive/22.05.tar.gz") {} }:
with pkgs;
let
    pythonBundle = python310.withPackages (ps: with ps; [ numpy matplotlib mypy ]);
in
mkShell {
    buildInputs = [ pythonBundle ];
}
