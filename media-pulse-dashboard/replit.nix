{ pkgs }: {
  deps = [
    pkgs.lsof
    pkgs.nodejs
    pkgs.nodePackages.npm
  ];
}
