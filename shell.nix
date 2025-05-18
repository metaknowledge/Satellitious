{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  packages = with pkgs; [
    (python3.withPackages(p: with p; [
      pygame
      # pyNumDiff
      # requests
      # pandas
    ]))
  ];

}
