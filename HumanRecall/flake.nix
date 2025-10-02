{
  description = "Python development environment with FastAPI";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        pythonPackages = pkgs.python3Packages;
        pythonEnv = pkgs.python3.withPackages (ps:
          with ps; with pkgs; [
            # Essential system libraries
            glibc
            stdenv.cc.cc.lib

            # Python and UV
            python312
            uv

            # Build tools
            gcc
            pkg-config

            # Common dependencies
            zlib
            libffi
            openssl
            ncurses
            readline
            sqlite
            tk
            xz

            # Development tools
            git
            curl
            wget
            which
            fastapi
            slowapi
            uvicorn
            pydantic
            python-multipart
            jinja2
            python-jose
            passlib
            bcrypt
            python-dotenv
            colorama
            pandas
            pyzmq
            matplotlib
          ]);
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            pythonEnv
            # Development tools
            python3Packages.pip
            python3Packages.setuptools
            python3Packages.wheel
            python3Packages.virtualenv
          ];
          shellHook = ''
            # Enable bash completion and case-insensitive completion
            if [ -f ${pkgs.bash-completion}/share/bash-completion/bash_completion ]; then
              source ${pkgs.bash-completion}/share/bash-completion/bash_completion
            fi

            export PYTHONWARNINGS="ignore"

            # Enable case-insensitive completion
            shopt -s nocaseglob
            shopt -s nocasematch
            bind "set completion-ignore-case on"
            bind "set show-all-if-ambiguous on"
            bind "set show-all-if-unmodified on"
            bind "set menu-complete-display-prefix on"

            # Create virtual environment if it doesn't exist
            if [ ! -d "venv" ]; then
              echo "Creating virtual environment..."
              python -m venv venv
            fi

            # Activate virtual environment
            source venv/bin/activate

            pip install ipykernel ipywidgets notebook

            # Install pocketbase if not already installed
            if ! python -c "import pocketbase" 2>/dev/null; then
              echo "Installing pocketbase..."
              pip install pocketbase
            fi

            python -m ipykernel install --user --name "$(basename $PWD)" --display-name "$(basename $PWD) (UV-FHS)"

          '';
        };
        packages.default = pythonEnv;
      });
}

