{
  description = "2pass by glopter and honeyfuggle";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-unstable";
    systems.url = "systems";
  };

  outputs = {
    self,
    nixpkgs,
    systems,
  }: let
    eachSystem = f: nixpkgs.lib.genAttrs (import systems) (system: f nixpkgs.legacyPackages.${system});
  in {
    packages = eachSystem (pkgs: {
      default = pkgs.writeShellApplication {
        name = "2pass";
        runtimeInputs = [
          pkgs.python3
          pkgs.ffmpeg
        ];
        text = ''python ${./2pass.py} "$@"'';
      };
    });
  };
}
