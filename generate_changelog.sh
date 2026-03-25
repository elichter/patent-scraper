#!/bin/bash
# generate_changelog.sh
# Usage: bash generate_changelog.sh v1.3.0
#
# Prerequisites: cargo install git-cliff
# Install cargo (Rust): curl https://sh.rustup.rs -sSf | sh
# Then: cargo install git-cliff

VERSION=$1

if [ -z "$VERSION" ]; then
    echo "Usage: bash generate_changelog.sh v1.3.0"
    exit 1
fi

echo "Generating CHANGELOG.md for $VERSION..."
git-cliff --tag "$VERSION" -o CHANGELOG.md

echo "Done. Review CHANGELOG.md then run:"
echo "  git add CHANGELOG.md"
echo "  git tag $VERSION"
echo "  git commit -m \"Release $VERSION\""
echo "  git push && git push --tags"
