#!/bin/bash
# Runs every check's two-direction test. Exits non-zero if any test fails.
#
# LOCAL DRIVER -- not shipped to consumers. precedent_materialize.py does not
# copy this file into a repo that resolves this source; it GENERATES its own
# tools/checks/tests/run_all.sh there, recorded in that repo's MANIFEST.json
# as "(generated)". Every source ships a driver, so copying one would force
# an arbitrary winner; generating sidesteps that, and lets the driver glob
# whatever THAT repo materialized. An edit here reaches this repo's own test
# runs only.
set -uo pipefail
cd "$(dirname "$0")"
status=0
for t in test_*.sh; do
  # A repo with no test_*.sh leaves the glob unexpanded; without this the
  # driver runs a file literally named test_*.sh and reports a failure that
  # is really an empty set. The generated driver carries the same guard.
  [ -e "$t" ] || continue
  echo "--- $t ---"
  if ! bash "$t"; then
    status=1
  fi
done
exit $status
