{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { nixpkgs, utils, ... }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};

      systems = {
        x86_64-linux = "linux_amd64";
      };

      kurtosis = pkgs.stdenv.mkDerivation rec {
        pname = "kurtosis-cli";
        version = "1.10.3";
        src = pkgs.fetchurl {
          url = "https://github.com/kurtosis-tech/kurtosis-cli-release-artifacts/releases/download/${version}/kurtosis-cli_${version}_${systems.${system}}.tar.gz";
          sha256 = "sha256-yDR7RuoSnQ4tZgNI5mAp/9ycZwaLxaZAbniqsiF7gxk=";
        };
        installPhase = ''
          mkdir -p $out/bin
          tar -xzf $src -C $out/bin
        '';
      };
    in
    {
      devShell = pkgs.mkShell {
        buildInputs = [
          kurtosis
        ];
      };
    }
  );
}
