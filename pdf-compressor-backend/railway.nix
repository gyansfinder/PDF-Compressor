{ pkgs }:
pkgs.mkShell {
  buildInputs = [ pkgs.ghostscript ];
}
