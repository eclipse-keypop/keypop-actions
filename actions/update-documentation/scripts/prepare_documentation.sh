#!/usr/bin/env bash

echo "Compute the current API version..."

repository_name=$1
version=$2

echo "Computed current API version: $version"

echo "Clone $repository_name..."
git clone "https://github.com/eclipse-keypop/${repository_name}.git"

cd "$repository_name" || exit 1

echo "Checkout doc branch..."
git checkout -f doc

echo "Delete existing SNAPSHOT directory..."
rm -rf *-SNAPSHOT

echo "Create target directory $version..."
mkdir "$version"

echo "Copy javadoc and uml files..."
cp -rf ../build/docs/javadoc/* "$version"/
cp -rf ../build/dokkaHtml/* "$version"/
cp -rf ../build/dokka/html/* "$version"/
cp -rf ../plugin/build/dokka/html/* "$version"/
cp -rf ../src/main/uml/api_*.svg "$version"/
cp -rf ../docs/uml/api_*.svg "$version"/
cp -rf ../docs/uml/class-diagram.svg "$version"/

# Find the latest stable version (first non-SNAPSHOT)
latest_stable=$(ls -d [0-9]*/ | grep -v SNAPSHOT | cut -f1 -d'/' | sort -Vr | head -n1)

# Create latest-stable copy if we have a stable version
if [ ! -z "$latest_stable" ]; then
    echo "Creating latest-stable directory pointing to $latest_stable..."
    rm -rf latest-stable
    mkdir latest-stable
    cp -rf "$latest_stable"/* latest-stable/
fi

echo "Update versions list..."
echo "| Available versions |" > list_versions.md
echo "|:---|" >> list_versions.md

# Get the list of directories sorted by version number
sorted_dirs=$(ls -d [0-9]*/ | cut -f1 -d'/' | sort -Vr)

# One column, and the version number is itself the link. There is exactly one document per
# version, so a second column would carry the same label on every row -- which also made every
# link of the page announce the same thing to a screen reader.
#
# Class diagrams are deliberately NOT linked from this page: they are published next to the
# documentation but reached only from its home page, so that each diagram is read in the context
# of the API it illustrates.
#
# Keep one version per line, and keep "(<version>)" in the link target: the central publication
# script retires an obsolete patch by deleting the line that mentions it.
for directory in $sorted_dirs
do
  badge=""
  if [ "$directory" = "$latest_stable" ]; then
      # The fixed link is the one to cite elsewhere, but the row shows the real version number.
      link='['"$directory"'](latest-stable "Fixed link to the latest stable version")'
      badge=' <span class="doc-badge doc-badge--stable">stable</span>'
  else
      link='['"$directory"']('"$directory"')'
      case "$directory" in
        *-SNAPSHOT) badge=' <span class="doc-badge doc-badge--snapshot">snapshot</span>' ;;
      esac
  fi
  echo "| $link$badge |" >> list_versions.md
done

# Names the table so the layout can size it by its content rather than stretch it across the page.
echo "{: .doc-versions}" >> list_versions.md

echo "Computed all versions:"
cat list_versions.md
cd ..
echo "Local docs update finished."