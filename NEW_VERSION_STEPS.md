Steps to pushing out a new version
==================================
1. Make sure that all tests are passing (`nosetests`)
2. Create new file in `/messages` and populate with release notes
3. Add entry to `messages.json`
4. Update version number in `README.md`
5. Commit and tag (e.g. v1.2.0)
6. Push
7. Copy change log text and paste into release on GitHub.com