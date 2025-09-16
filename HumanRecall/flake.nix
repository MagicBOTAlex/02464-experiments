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
          with ps; [
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

            # Install pocketbase if not already installed
            if ! python -c "import pocketbase" 2>/dev/null; then
              echo "Installing pocketbase..."
              pip install pocketbase
            fi

            alias run="uvicorn main:app --reload"
            echo "Python FastAPI development environment"
            echo "Python version: $(python --version)"
            echo "Virtual environment: $(which python)"
            echo "FastAPI available with uvicorn server"
            echo ""
            echo "To create a simple FastAPI app:"
            echo "  echo 'from fastapi import FastAPI; app = FastAPI(); @app.get(\"/\"); def read_root(): return {\"Hello\": \"World\"}' > main.py"
            echo "  run"
            echo ""
            echo "Available aliases:"
            echo "  run - uvicorn main:app --reload"'';
        };
        packages.default = pythonEnv;
      });
}

