"""Put all recording parts and the manifest beside this script, then run it."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'recordings-manifest.json').read_text())
target=root/'recordings.zip'
if target.exists():raise SystemExit('recordings.zip already exists; move it before reassembling.')
pending=root/'recordings.zip.tmp';whole=hashlib.sha256()
try:
 with pending.open('wb') as out:
  for part in manifest['parts']:
   name=part['file']
   if Path(name).name!=name:raise ValueError('Invalid part filename')
   data=(root/name).read_bytes()
   if len(data)!=part['bytes'] or hashlib.sha256(data).hexdigest()!=part['sha256']:raise ValueError('Missing or corrupt part: '+name)
   out.write(data);whole.update(data)
 if whole.hexdigest()!=manifest['sha256']:raise ValueError('Complete archive checksum mismatch')
 pending.rename(target)
except BaseException:
 pending.unlink(missing_ok=True)
 raise
print('Verified recordings.zip; extract it to inspect the complete recordings and source history.')
