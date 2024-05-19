# shell.nix

with import <nixpkgs> { };
let
  pythonPackages = python311Packages;
in pkgs.mkShell rec {
  name = "tensorflowEnv";
  buildInputs = [
    pythonPackages.python
    pythonPackages.matplotlib
    pythonPackages.jupyter
    pythonPackages.tqdm
    pythonPackages.ollama
  ];
}
