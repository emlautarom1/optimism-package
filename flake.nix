{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};

      kurtosis = pkgs.stdenv.mkDerivation {
        pname = "kurtosis-cli";
        version = "1.10.3";
        src = pkgs.fetchurl {
          url = "https://github.com/kurtosis-tech/kurtosis-cli-release-artifacts/releases/download/1.10.3/kurtosis-cli_1.10.3_linux_amd64.tar.gz";
          sha256 = "replace-with-actual-sha256";
        };
        installPhase = ''
          mkdir -p $out/bin
          tar -xzf $src -C $out/bin
        '';
      };
    in
    {
      devShell = pkgs.mkShell {
        buildInputs = with pkgs; [
        ];
      };
    }
  );
}
