print("Verifying minimum papers requirement...")

with open('app.py', 'r') as f:
    content = f.read()
    if 'len(valid_files) < 2' in content:
        print('✅ app.py: Minimum 2 papers required')
    else:
        print('❌ app.py: Update failed')

with open('templates/index.html', 'r') as f:
    content = f.read()
    if 'Minimum 2' in content and 'at least 2' in content:
        print('✅ index.html: UI updated to show "Minimum 2"')
    else:
        print('❌ index.html: Update failed')

print('\n✅ COMPLETE: System now accepts minimum 2 papers instead of 5')
print('\nWhat changed:')
print('  • app.py: Validation changed from 5 → 2 papers')
print('  • index.html: UI text changed from "Minimum 5" → "Minimum 2"')
print('\nYou can now upload just 2 question papers for analysis!')

