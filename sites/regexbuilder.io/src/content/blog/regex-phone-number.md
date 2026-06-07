---
title: "Regex Phone Number Validation: Patterns, Pitfalls, and Best Practices"
description: "Learn regex patterns for US and international phone number validation. Covers E.164, common formats, when NOT to use regex, and tested working patterns."
publishDate: 2026-06-07
updatedDate: 2026-06-07
author: "Editorial Team"
tags: ["regex", "phone number", "validation", "E.164", "form validation"]
draft: false
---

Phone number validation with regex is notoriously tricky. Unlike email addresses, phone numbers have no single global standard — they vary by country, carrier, and era, with different digit counts, separators, optional area codes, and extension formats. This guide covers practical patterns, their limitations, and when to reach for a dedicated library instead.

## Why phone number regex is hard

A quick survey of valid phone number formats illustrates the challenge:

```
5558675309           US, no separators, no area code
555-867-5309         US with dashes
(555) 867-5309       US with parenthesized area code
555.867.5309         US with dots
+1-555-867-5309      US with country code
+1 (555) 867-5309    US with country code and spaces
+44 20 7946 0958     UK London number
+49 30 12345678      Germany
+86 138 1234 5678    China mobile
+81 3-1234-5678      Japan
0800 123 456         UK freephone
800-555-1234 ext 42  US with extension
800-555-1234 x42     US with short extension notation
```

No single regex handles all of these correctly. The goal is to choose the right pattern for your specific use case.

## Basic US phone patterns

### Strict 10-digit US format

Matches 10 digits with common separators (dashes, dots, spaces) and optional parentheses around the area code.

```regex
^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$
```

This matches:
- `5558675309`
- `555-867-5309`
- `(555) 867-5309`
- `555.867.5309`
- `555 867 5309`

```python
import re

us_phone = re.compile(r'^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$')

test_numbers = [
    '5558675309',
    '555-867-5309',
    '(555) 867-5309',
    '555.867.5309',
    '(555)867-5309',
    '555 867 5309',
    '+15558675309',   # will NOT match — no country code support
]

for number in test_numbers:
    m = us_phone.match(number)
    if m:
        print(f'{number!r:25} -> area={m.group(1)} prefix={m.group(2)} line={m.group(3)}')
    else:
        print(f'{number!r:25} -> NO MATCH')
```

Output:
```
'5558675309'              -> area=555 prefix=867 line=5309
'555-867-5309'            -> area=555 prefix=867 line=5309
'(555) 867-5309'          -> area=555 prefix=867 line=5309
'555.867.5309'            -> area=555 prefix=867 line=5309
'(555)867-5309'           -> area=555 prefix=867 line=5309
'555 867 5309'            -> area=555 prefix=867 line=5309
'+15558675309'            -> NO MATCH
```

### US format with optional country code

```regex
^(\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$
```

Now also matches:
- `+15558675309`
- `+1-555-867-5309`
- `1 (555) 867-5309`

```python
us_with_cc = re.compile(
    r'^(\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$'
)
```

### US format with optional extension

```regex
^(\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})(\s*(ext|x|ext\.)\s*(\d{1,5}))?$
```

Handles extensions like:
- `555-867-5309 ext 42`
- `555-867-5309 x100`
- `555-867-5309 ext.200`

```python
us_with_ext = re.compile(
    r'^(\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})'
    r'(\s*(ext|x|ext\.)\s*(\d{1,5}))?$',
    re.IGNORECASE
)

print(bool(us_with_ext.match('(555) 867-5309 ext 42')))  # True
print(bool(us_with_ext.match('555-867-5309 x100')))       # True
print(bool(us_with_ext.match('555-867-5309 EXT.200')))    # True
```

## International E.164 format

The ITU-T E.164 standard defines an international phone number format used by telecom systems, SMS APIs, and most cloud telephony providers. It is the most interoperable format.

E.164 format: `+` followed by up to 15 digits, no separators.

```regex
^\+[1-9]\d{6,14}$
```

Breakdown:
- `\+` — literal plus sign (country code prefix)
- `[1-9]` — first digit of country code must be 1-9 (no leading zero)
- `\d{6,14}` — remaining digits (minimum total 7, maximum 15)

```python
e164_pattern = re.compile(r'^\+[1-9]\d{6,14}$')

valid = [
    '+15558675309',     # US
    '+447911123456',    # UK
    '+4930123456',      # Germany
    '+818012345678',    # Japan
    '+8613912345678',   # China
]

invalid = [
    '+05558675309',     # leading zero in country code
    '+1',               # too short
    '+1' + '0' * 15,    # too long
    '15558675309',      # missing + prefix
]

for n in valid:
    print(f'{n} -> {bool(e164_pattern.match(n))}')
# All True

for n in invalid:
    print(f'{n} -> {bool(e164_pattern.match(n))}')
# All False
```

## Flexible international pattern

For user-facing input that might include spaces, dashes, or parentheses alongside a country code:

```regex
^\+?[1-9]\d{0,2}[-.\s]?\(?\d{1,4}\)?(?:[-.\s]?\d{1,4}){2,5}$
```

This is intentionally permissive — it accepts most formats a human would enter. Run it through your validation layer; the result is not a guarantee of a real, reachable number.

```javascript
const flexInternational = /^\+?[1-9]\d{0,2}[-.\s]?\(?\d{1,4}\)?(?:[-.\s]?\d{1,4}){2,5}$/;

const numbers = [
    '+1 (555) 867-5309',
    '+44 20 7946 0958',
    '+49 30 1234 5678',
    '+86 138 1234 5678',
    '+81 3-1234-5678',
];

numbers.forEach(n => console.log(n, '->', flexInternational.test(n)));
// All true
```

## Normalizing phone numbers with regex

Before validation, strip all formatting to compare or store numbers consistently:

```python
import re

def normalize_to_e164(raw: str, default_country_code: str = '+1') -> str:
    """Strip formatting and return E.164-ish number."""
    # Remove all non-digit characters except leading +
    digits_only = re.sub(r'[^\d+]', '', raw)

    # If starts with +, assume it's already international
    if digits_only.startswith('+'):
        return digits_only

    # Strip leading country code 1 for US numbers
    if digits_only.startswith('1') and len(digits_only) == 11:
        return '+' + digits_only

    # 10-digit US number — add default country code
    if len(digits_only) == 10:
        return default_country_code + digits_only

    return digits_only  # return as-is if we can't determine format

print(normalize_to_e164('(555) 867-5309'))    # '+15558675309'
print(normalize_to_e164('+1-555-867-5309'))   # '+15558675309'
print(normalize_to_e164('555.867.5309'))      # '+15558675309'
```

## When NOT to use regex for phone validation

Regex can tell you a string *looks like* a phone number. It cannot tell you:

- Whether the number is assigned to an actual subscriber
- Whether it's a mobile or landline number
- Whether the country code and subscriber number combination is valid for that country (each country has different number length rules)
- Whether the number has been disconnected or recycled

For production applications that need real phone validation — especially for SMS delivery, two-factor authentication, or fraud prevention — use a dedicated library.

### libphonenumber (Google)

Google's `libphonenumber` is the gold standard for phone validation. It knows every country's numbering plan rules.

**Python (phonenumbers library):**

```python
import phonenumbers
from phonenumbers import NumberParseException

def validate_phone(raw: str, region: str = 'US') -> dict:
    try:
        parsed = phonenumbers.parse(raw, region)
        return {
            'valid': phonenumbers.is_valid_number(parsed),
            'possible': phonenumbers.is_possible_number(parsed),
            'e164': phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            ),
            'national': phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.NATIONAL
            ),
            'type': str(phonenumbers.number_type(parsed)),
        }
    except NumberParseException as e:
        return {'valid': False, 'error': str(e)}

print(validate_phone('(555) 867-5309'))
# {'valid': True, 'possible': True, 'e164': '+15558675309', ...}
```

**JavaScript:**

```javascript
import { parsePhoneNumber } from 'libphonenumber-js';

const phone = parsePhoneNumber('(555) 867-5309', 'US');
console.log(phone.isValid());           // true
console.log(phone.format('E.164'));     // '+15558675309'
console.log(phone.getType());          // 'FIXED_LINE_OR_MOBILE'
```

## Summary: which pattern to use

| Use case | Recommended approach |
|----------|---------------------|
| US-only web form, simple validation | `^\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})$` |
| US with country code and extension | Full US pattern with optional groups |
| International input, store as E.164 | Flexible pattern + normalize to E.164 |
| SMS delivery / 2FA / fraud checks | Use `libphonenumber` (not regex) |
| Normalizing stored numbers | Strip non-digits, apply E.164 rules |
| Log scanning / data extraction | Flexible pattern, false positives acceptable |

## Practical JavaScript form validation

```javascript
function validatePhoneInput(input) {
  // Strip whitespace first
  const cleaned = input.trim();

  // E.164 stored format
  const e164 = /^\+[1-9]\d{6,14}$/;
  if (e164.test(cleaned)) return { valid: true, format: 'e164' };

  // US format with optional country code
  const us = /^(\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})(\s*(ext|x|ext\.)\s*(\d{1,5}))?$/i;
  if (us.test(cleaned)) return { valid: true, format: 'us' };

  return { valid: false, format: null };
}

console.log(validatePhoneInput('(555) 867-5309'));       // { valid: true, format: 'us' }
console.log(validatePhoneInput('+447911123456'));         // { valid: true, format: 'e164' }
console.log(validatePhoneInput('not a phone'));           // { valid: false, format: null }
```

Test your phone number patterns against real inputs at [regexbuilder.io](/) to verify they handle the edge cases your users will throw at them.
