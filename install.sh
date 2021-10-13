#!/bin/bash


i() {
    mkdir -p "$prefix/$dest"

    for file in "$src"/*; do
        cp -v "$file" "$prefix/$dest/"
    done
}

u() {
    [ -d "$prefix/$dest" ] || exit 1

    for file in "$src"/*; do
        rm -v "$prefix/$dest/${file##*/}"
    done
}

main() {
    prefix=$HOME
    src=scripts
    dest=bin

    case $1 in
        install) i ;;
        uninstall) u ;;
    esac

    printf "\nAdd ${prefix}/${dest} to your PATH\n"
}

main "$@"
