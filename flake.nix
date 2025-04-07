{
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/5ed627539ac84809c78b2dd6d26a5cebeb5ae269";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        foundry = pkgs.stdenv.mkDerivation {
          pname = "foundry";
          version = "stable";

          src = pkgs.fetchurl {
            url = "https://github.com/foundry-rs/foundry/releases/download/stable/foundry_stable_linux_amd64.tar.gz";
            sha256 = "sha256-1hG+7ruDs0sDsg5DrlmOuj8nRXRT9Qkz3a5WPPF1pNc=";
          };

          dontUnpack = true;

          installPhase = ''
            mkdir -p $out/bin
            tar -xzf $src -C $out/bin
          '';
        };

        kurtosis = pkgs.stdenv.mkDerivation rec {
          pname = "kurtosis";
          version = "1.4.4";

          src = pkgs.fetchurl {
            url = "https://github.com/kurtosis-tech/kurtosis-cli-release-artifacts/releases/download/${version}/kurtosis-cli_${version}_linux_amd64.tar.gz";
            sha256 = "sha256-wQxQjDdQxJkYuiSLeoQCmA7hLIfKmBnszQgPUZlM4KY=";
          };

          installPhase = ''
            mkdir -p $out/bin
            tar -xzf $src -C $out/bin/
          '';
        };

        tx-fuzz = pkgs.buildGoModule rec {
          pname = "tx-fuzz";
          version = "1.4.0";

          src = pkgs.fetchFromGitHub {
            owner = "MariusVanDerWijden";
            repo = "tx-fuzz";
            rev = "v${version}";
            hash = "sha256-CqxCquPfxyKL6ck7YCnpq9Yj2jdBOO36xf9ojIr/0bk=";
          };

          subPackages = [ "cmd/livefuzzer" ];

          vendorHash = "sha256-s5cbutqpaXhNRT4HORrSmSLelQAzQCgkyLRJfM66bHQ=";
          doCheck = false;
        };

        kurtosis-test = pkgs.stdenv.mkDerivation rec {
          pname = "kurtosis-test";
          version = "0.0.2";

          src = pkgs.fetchurl {
            url = "https://github.com/ethereum-optimism/kurtosis-test/releases/download/v${version}/kurtosis-test_Linux_x86_64.tar.gz";
            sha256 = "sha256-DKoXlawx0V4obMfCwB96cAdynJUXA3gA3AcjPiltsno=";
          };

          dontUnpack = true;

          installPhase = ''
            mkdir -p $out/bin
            tar -xzf $src -C $out/bin/
          '';
        };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = [
            kurtosis
            foundry
            tx-fuzz
            kurtosis-test
            pkgs.python3
            pkgs.shellcheck
            pkgs.watchexec
          ];
        };
      }
    );
}
