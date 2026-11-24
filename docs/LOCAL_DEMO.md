# Local Web Demo

Launch the isolated local browser workbench on loopback (`127.0.0.1`):

```sh
sidinspector demo --port 8765
# or:
python3 tools/serve_demo.py --port 8765
```

Open <http://127.0.0.1:8765> in a browser.

## Security & Isolation Guarantees

- Binds to `127.0.0.1` by default and validates `Host` and `Origin` headers.
- Serves HTML with a per-request CSP script nonce and `X-Content-Type-Options: nosniff`.
- Each **Run all workflows** request copies the manifest-tracked files into a fresh temporary directory, checks SHA-256 hashes, executes the released Python workflow in an isolated subprocess (`python3 -I -B`), and removes the temporary directory automatically.
- Custom CSV audits in the local demo execute purely in-memory against bounded row limits and never write user data into the repository tree.
