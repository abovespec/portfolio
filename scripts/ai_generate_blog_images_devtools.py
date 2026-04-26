#!/usr/bin/env python3
"""
AI blog image generator — dev/text utility sites (Phase-3).
Covers 16 sites: caseconvert, citefast, crontab, cssminify, encodeonline,
gradientcss, htmlformat, jwtinspect, passwordgen, qrcodegen, regexbuilder,
sqlformat, textdiff, utmbuilder, uuidgen, wordcounttools.

Treatment: lighter than YMYL — 1 OG default (1200x630) + 1 hero per article (1200x630).
No body images.

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_devtools.py --site caseconvert.io --all
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_devtools.py --batch a
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_devtools.py --batch b
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_devtools.py --all-sites
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

SIZES = {"hero": (1200, 630)}

SITE_MANIFESTS = {
    # -----------------------------------------------------------------------
    "caseconvert.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/caseconvert.io/public",
            "prompt": (
                "Code editor showing a string variable in multiple case formats — "
                "camelCase snake_case PascalCase kebab-case — syntax highlighted, "
                "dark terminal theme, developer tool editorial"
            ),
        },
        {
            "slug": "camelcase-to-snake-case-javascript-hero",
            "size": "hero",
            "prompt": (
                "JavaScript code editor showing camelCase variable being converted "
                "to snake_case with a replace function, dark syntax-highlighted theme, "
                "developer editorial"
            ),
        },
        {
            "slug": "camelcase-to-snake-case-python-hero",
            "size": "hero",
            "prompt": (
                "Python IDE showing camelCase to snake_case string conversion "
                "with re.sub pattern, dark terminal monospace theme, developer editorial"
            ),
        },
        {
            "slug": "camelcase-vs-snake-case-hero",
            "size": "hero",
            "prompt": (
                "Split code editor pane — camelCase variable names on left "
                "and snake_case equivalents on right, dark syntax highlighted, "
                "developer comparison editorial"
            ),
        },
        {
            "slug": "naming-conventions-programming-hero",
            "size": "hero",
            "prompt": (
                "Programming naming conventions reference card showing camelCase "
                "snake_case PascalCase kebab-case SCREAMING_SNAKE with examples, "
                "dark developer editorial, clean code reference"
            ),
        },
        {
            "slug": "string-to-camelcase-javascript-hero",
            "size": "hero",
            "prompt": (
                "JavaScript code editor showing a toCamelCase utility function "
                "implementation with example input and output in comments, "
                "dark syntax-highlighted developer editorial"
            ),
        },
        {
            "slug": "what-is-snake-case-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing snake_case variable names with underscores "
                "visually highlighted, dark monospace theme, developer editorial, "
                "clean code illustration"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "citefast.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/citefast.io/public",
            "prompt": (
                "Academic reference list on clean white paper showing APA MLA Chicago "
                "formatted citations, open book beside it, educational editorial, "
                "clean scholarly aesthetic"
            ),
        },
        {
            "slug": "apa-citation-format-hero",
            "size": "hero",
            "prompt": (
                "APA 7th edition citation format guide on clean white paper, "
                "author date title journal format visible, academic educational editorial, "
                "clean scholarly aesthetic"
            ),
        },
        {
            "slug": "bibliography-vs-works-cited-hero",
            "size": "hero",
            "prompt": (
                "Side-by-side comparison of Bibliography page and Works Cited page "
                "in academic format on clean paper, educational editorial"
            ),
        },
        {
            "slug": "chicago-citation-style-hero",
            "size": "hero",
            "prompt": (
                "Chicago Manual of Style citation on clean paper showing footnote "
                "and bibliography format, academic scholarly editorial, clean design"
            ),
        },
        {
            "slug": "how-to-cite-a-book-hero",
            "size": "hero",
            "prompt": (
                "Open book with a citation reference card beside it showing "
                "APA MLA Chicago format examples, academic editorial, clean scholarly"
            ),
        },
        {
            "slug": "how-to-cite-a-website-hero",
            "size": "hero",
            "prompt": (
                "Laptop displaying a website with a citation format card overlaid "
                "showing URL author date access format, academic editorial, clean"
            ),
        },
        {
            "slug": "mla-citation-format-hero",
            "size": "hero",
            "prompt": (
                "MLA 9th edition Works Cited page on clean white paper, "
                "hanging indent and alphabetical entries visible, academic editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "crontab.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/crontab.io/public",
            "prompt": (
                "Terminal window showing crontab -e command with a cron schedule entry, "
                "dark monospace font, scheduled task concept, developer editorial"
            ),
        },
        {
            "slug": "cron-expression-examples-hero",
            "size": "hero",
            "prompt": (
                "Terminal or code editor showing a list of cron expressions "
                "with schedule descriptions as comments, dark monospace developer editorial"
            ),
        },
        {
            "slug": "cron-job-not-running-hero",
            "size": "hero",
            "prompt": (
                "Linux terminal showing cron log and systemctl status output "
                "for debugging a failed cron job, dark monospace developer editorial"
            ),
        },
        {
            "slug": "crontab-every-5-minutes-hero",
            "size": "hero",
            "prompt": (
                "Terminal showing crontab entry with asterisk-slash-5 interval expression "
                "highlighted, dark monospace developer editorial"
            ),
        },
        {
            "slug": "crontab-syntax-hero",
            "size": "hero",
            "prompt": (
                "Crontab syntax reference card annotating the five fields — "
                "minute hour day month weekday — with labels and example values, "
                "clean developer reference card"
            ),
        },
        {
            "slug": "how-to-schedule-a-cron-job-hero",
            "size": "hero",
            "prompt": (
                "Linux terminal showing step-by-step crontab -e setup with "
                "a new cron job being added, dark monospace developer tutorial editorial"
            ),
        },
        {
            "slug": "linux-crontab-tutorial-hero",
            "size": "hero",
            "prompt": (
                "Linux terminal with crontab -l listing showing multiple scheduled jobs, "
                "dark monospace developer editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "cssminify.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/cssminify.io/public",
            "prompt": (
                "Split pane code editor — formatted readable CSS on left "
                "versus minified single-line CSS on right, dark syntax highlighted, "
                "developer tool editorial"
            ),
        },
        {
            "slug": "critical-css-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing critical CSS inlined in HTML head tag, "
                "render-blocking optimization concept, dark syntax highlighted developer editorial"
            ),
        },
        {
            "slug": "css-file-size-too-large-hero",
            "size": "hero",
            "prompt": (
                "Browser DevTools Network tab showing an oversized CSS file "
                "with file size highlighted, developer debugging editorial, dark theme"
            ),
        },
        {
            "slug": "css-optimization-techniques-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing optimized CSS with selector efficiency techniques, "
                "unused rule removal, dark syntax highlighted developer editorial"
            ),
        },
        {
            "slug": "how-to-minify-css-hero",
            "size": "hero",
            "prompt": (
                "Terminal or tool interface showing CSS before and after minification "
                "with file size comparison, dark developer editorial"
            ),
        },
        {
            "slug": "minify-css-webpack-hero",
            "size": "hero",
            "prompt": (
                "webpack.config.js open in editor with CSS minification plugin "
                "configuration code visible, dark developer editorial"
            ),
        },
        {
            "slug": "remove-unused-css-hero",
            "size": "hero",
            "prompt": (
                "Browser DevTools Coverage tab showing unused CSS percentage "
                "highlighted in red, developer optimization editorial, dark theme"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "encodeonline.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/encodeonline.io/public",
            "prompt": (
                "Terminal showing Base64 encode and hash operations side by side, "
                "dark monospace font, developer encoding tool editorial"
            ),
        },
        {
            "slug": "base64-encoding-explained-hero",
            "size": "hero",
            "prompt": (
                "Terminal showing a string being Base64 encoded and decoded "
                "step by step, dark monospace developer editorial"
            ),
        },
        {
            "slug": "base64-vs-hex-hero",
            "size": "hero",
            "prompt": (
                "Side-by-side terminal comparison of Base64 encoded output "
                "versus hex encoded output for the same binary data, "
                "dark monospace developer editorial"
            ),
        },
        {
            "slug": "hash-functions-explained-hero",
            "size": "hero",
            "prompt": (
                "Terminal showing MD5 SHA-1 SHA-256 hash outputs for the same "
                "input string, increasing hash lengths visible, "
                "dark monospace developer editorial"
            ),
        },
        {
            "slug": "html-entities-guide-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing HTML special characters and their entity "
                "equivalents — ampersand less-than greater-than — dark syntax highlighted"
            ),
        },
        {
            "slug": "md5-hash-explained-hero",
            "size": "hero",
            "prompt": (
                "Terminal showing md5sum command with a 32-character hex hash output, "
                "dark monospace developer editorial, hash string prominently displayed"
            ),
        },
        {
            "slug": "url-encoding-guide-hero",
            "size": "hero",
            "prompt": (
                "Code editor or terminal showing a URL with special characters "
                "and their percent-encoded equivalents highlighted, "
                "dark developer editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "gradientcss.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/gradientcss.io/public",
            "prompt": (
                "CSS gradient generator interface with code editor showing "
                "gradient properties and a colorful gradient preview, "
                "modern developer tool editorial"
            ),
        },
        {
            "slug": "css-gradient-animation-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing CSS keyframes gradient animation with "
                "colorful shifting gradient preview strip beside it, "
                "dark developer editorial"
            ),
        },
        {
            "slug": "css-gradient-background-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing CSS background gradient properties for a "
                "full-page hero section with a colorful gradient preview, "
                "dark syntax highlighted"
            ),
        },
        {
            "slug": "css-gradient-hero",
            "size": "hero",
            "prompt": (
                "Three gradient swatches side by side — linear radial conic — "
                "with their CSS syntax shown below each, colorful clean developer editorial"
            ),
        },
        {
            "slug": "css-gradient-text-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing CSS gradient applied to text using "
                "background-clip text property, colorful gradient text result preview, "
                "dark developer editorial"
            ),
        },
        {
            "slug": "linear-gradient-css-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing CSS linear-gradient syntax with direction "
                "and color stops, horizontal gradient color bar preview, "
                "dark syntax highlighted developer editorial"
            ),
        },
        {
            "slug": "radial-gradient-css-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing CSS radial-gradient syntax creating a "
                "spotlight or circle effect, radial color preview, "
                "dark developer editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "htmlformat.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/htmlformat.io/public",
            "prompt": (
                "Split-pane code editor with messy unformatted HTML on the left "
                "and clean indented HTML on the right, dark syntax highlighted, "
                "HTML formatter tool editorial"
            ),
        },
        {
            "slug": "how-to-format-html-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing properly indented nested HTML with consistent "
                "2-space indentation, dark syntax highlighted developer editorial"
            ),
        },
        {
            "slug": "html-beautifier-guide-hero",
            "size": "hero",
            "prompt": (
                "Code editor before-and-after showing minified HTML on top "
                "and beautifully indented HTML below after beautification, dark theme"
            ),
        },
        {
            "slug": "html-indentation-best-practices-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing HTML with correct nested indentation structure, "
                "indentation guides visible, dark syntax highlighted developer editorial"
            ),
        },
        {
            "slug": "html-minification-hero",
            "size": "hero",
            "prompt": (
                "Two file size comparison showing HTML file before and after minification, "
                "file size reduction percentage displayed, dark developer editorial"
            ),
        },
        {
            "slug": "prettier-html-formatting-hero",
            "size": "hero",
            "prompt": (
                "VS Code editor with .prettierrc configuration file open showing "
                "HTML formatting options, dark developer editorial"
            ),
        },
        {
            "slug": "validate-html-hero",
            "size": "hero",
            "prompt": (
                "W3C HTML validator results page showing green validation pass "
                "with no errors found, developer tool editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "jwtinspect.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/jwtinspect.io/public",
            "prompt": (
                "JWT token string split into three color-coded parts — "
                "red header purple payload blue signature — on dark background, "
                "developer security tool editorial"
            ),
        },
        {
            "slug": "how-jwt-authentication-works-hero",
            "size": "hero",
            "prompt": (
                "Abstract diagram showing JWT authentication flow — "
                "client login, server signs token, client sends token with requests, "
                "dark developer editorial"
            ),
        },
        {
            "slug": "jwt-claims-explained-hero",
            "size": "hero",
            "prompt": (
                "JWT payload JSON object showing iss sub aud exp iat nbf jti "
                "claim fields with values, dark terminal theme, developer editorial"
            ),
        },
        {
            "slug": "jwt-security-best-practices-hero",
            "size": "hero",
            "prompt": (
                "Security checklist in code comment format listing JWT best practices "
                "with checkmarks, dark developer editorial, security engineering aesthetic"
            ),
        },
        {
            "slug": "jwt-token-expiration-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing JWT access token and refresh token rotation logic, "
                "token expiration handling, dark developer editorial"
            ),
        },
        {
            "slug": "jwt-vs-session-hero",
            "size": "hero",
            "prompt": (
                "Side-by-side abstract comparison of JWT stateless token flow "
                "versus session cookie flow, dark developer diagram editorial"
            ),
        },
        {
            "slug": "what-is-a-jwt-token-hero",
            "size": "hero",
            "prompt": (
                "JWT token string prominently displayed split into three parts "
                "with labels — header payload signature — on dark background, "
                "clean developer educational editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "passwordgen.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/passwordgen.io/public",
            "prompt": (
                "Terminal or password generator interface showing a random "
                "strong password with mixed characters displayed, "
                "dark monospace security tool editorial"
            ),
        },
        {
            "slug": "how-are-passwords-hashed-hero",
            "size": "hero",
            "prompt": (
                "Terminal showing bcrypt hash output alongside a plaintext password, "
                "password hashing concept, dark monospace developer editorial"
            ),
        },
        {
            "slug": "how-to-create-a-strong-password-hero",
            "size": "hero",
            "prompt": (
                "Password strength meter showing a strong password with "
                "complexity indicators — uppercase numbers symbols — "
                "clean security tool editorial"
            ),
        },
        {
            "slug": "passphrase-vs-password-hero",
            "size": "hero",
            "prompt": (
                "Side-by-side comparison showing a complex random password "
                "versus a memorable multi-word passphrase, "
                "security comparison editorial, clean design"
            ),
        },
        {
            "slug": "password-generator-guide-hero",
            "size": "hero",
            "prompt": (
                "Password generator tool interface with length slider and "
                "character type checkboxes visible, dark security tool editorial"
            ),
        },
        {
            "slug": "password-manager-comparison-hero",
            "size": "hero",
            "prompt": (
                "Clean comparison table or icon grid showing password manager "
                "options with feature columns, security software editorial"
            ),
        },
        {
            "slug": "what-makes-a-good-password-hero",
            "size": "hero",
            "prompt": (
                "Password entropy visualization showing strength by length "
                "and character set size, clean security educational editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "qrcodegen.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/qrcodegen.io/public",
            "prompt": (
                "Clean black and white QR code displayed prominently on white background "
                "beside a simple generator interface, modern minimal tool editorial"
            ),
        },
        {
            "slug": "dynamic-vs-static-qr-code-hero",
            "size": "hero",
            "prompt": (
                "Side-by-side comparison of dynamic QR code with edit arrow "
                "versus static QR code with lock icon, clean QR editorial"
            ),
        },
        {
            "slug": "how-qr-codes-work-hero",
            "size": "hero",
            "prompt": (
                "Technical diagram showing QR code structure with labeled regions — "
                "finder patterns timing patterns data modules — educational editorial"
            ),
        },
        {
            "slug": "how-to-create-a-qr-code-hero",
            "size": "hero",
            "prompt": (
                "Simple step-by-step visual showing URL input field "
                "and resulting QR code output, clean minimal tool editorial"
            ),
        },
        {
            "slug": "qr-code-best-practices-hero",
            "size": "hero",
            "prompt": (
                "QR code design examples showing proper size quiet zone and "
                "contrast requirements, clean QR design editorial"
            ),
        },
        {
            "slug": "qr-code-for-website-hero",
            "size": "hero",
            "prompt": (
                "Smartphone scanning a QR code that links to a website, "
                "modern clean tech editorial photography, minimal background"
            ),
        },
        {
            "slug": "qr-code-in-html-css-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing JavaScript QR code generation snippet "
                "with a small rendered QR code output preview, dark developer editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "regexbuilder.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/regexbuilder.io/public",
            "prompt": (
                "Regex pattern in a code editor with matched text highlighted "
                "in color below, dark developer tool editorial, abstract pattern matching"
            ),
        },
        {
            "slug": "how-to-use-regex-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing a regex pattern being tested against "
                "sample strings with color-highlighted match results, dark theme"
            ),
        },
        {
            "slug": "regex-cheatsheet-hero",
            "size": "hero",
            "prompt": (
                "Regex quick reference cheatsheet card showing character classes "
                "quantifiers anchors and groups in monospace font, dark developer editorial"
            ),
        },
        {
            "slug": "regex-email-validation-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing an email regex pattern with valid "
                "and invalid test email addresses below with match indicators, "
                "dark developer editorial"
            ),
        },
        {
            "slug": "regex-groups-capturing-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing regex with numbered capturing groups "
                "and the extracted group values in output, dark developer editorial"
            ),
        },
        {
            "slug": "regex-lookahead-lookbehind-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing lookahead and lookbehind regex syntax "
                "with annotation labels, dark developer editorial, pattern matching"
            ),
        },
        {
            "slug": "regex-tutorial-hero",
            "size": "hero",
            "prompt": (
                "Regex pattern breakdown diagram with each component annotated — "
                "anchors quantifiers character classes — dark developer editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "sqlformat.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/sqlformat.io/public",
            "prompt": (
                "SQL query in a code editor with clean formatting and "
                "syntax-highlighted keywords SELECT FROM WHERE, dark developer editorial"
            ),
        },
        {
            "slug": "explain-plan-sql-hero",
            "size": "hero",
            "prompt": (
                "SQL EXPLAIN plan output in terminal showing query execution steps "
                "and cost estimates, dark monospace developer editorial"
            ),
        },
        {
            "slug": "how-to-format-sql-hero",
            "size": "hero",
            "prompt": (
                "Before-and-after SQL formatting — compressed single-line query "
                "above and formatted readable multi-line query below, dark developer editorial"
            ),
        },
        {
            "slug": "sql-joins-explained-hero",
            "size": "hero",
            "prompt": (
                "Venn diagram style visualization showing SQL INNER LEFT RIGHT "
                "FULL JOIN relationships with table set representations, "
                "clean developer educational editorial"
            ),
        },
        {
            "slug": "sql-query-optimization-hero",
            "size": "hero",
            "prompt": (
                "Database index schema and query plan visualization showing "
                "optimized query path, dark technical developer editorial"
            ),
        },
        {
            "slug": "sql-style-guide-hero",
            "size": "hero",
            "prompt": (
                "SQL style guide code card showing uppercase keywords "
                "and aligned column formatting conventions, dark developer editorial"
            ),
        },
        {
            "slug": "sql-vs-nosql-hero",
            "size": "hero",
            "prompt": (
                "Side-by-side comparison of SQL table schema on the left "
                "versus NoSQL JSON document structure on the right, "
                "dark developer editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "textdiff.pro": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/textdiff.pro/public",
            "prompt": (
                "Split diff view showing two text versions side by side "
                "with added lines highlighted green and removed lines red, "
                "developer tool editorial"
            ),
        },
        {
            "slug": "compare-strings-python-hero",
            "size": "hero",
            "prompt": (
                "Python code editor showing string comparison using difflib "
                "with diff output displayed, dark developer editorial"
            ),
        },
        {
            "slug": "compare-two-text-files-linux-hero",
            "size": "hero",
            "prompt": (
                "Linux terminal showing diff command output comparing two text files, "
                "added and removed lines visible, dark monospace editorial"
            ),
        },
        {
            "slug": "git-diff-explained-hero",
            "size": "hero",
            "prompt": (
                "Terminal showing git diff output with green addition lines "
                "and red deletion lines, dark developer editorial, version control aesthetic"
            ),
        },
        {
            "slug": "how-does-diff-work-hero",
            "size": "hero",
            "prompt": (
                "Abstract diagram showing two text sequences being compared "
                "with common subsequences highlighted, developer algorithm editorial"
            ),
        },
        {
            "slug": "myers-diff-algorithm-hero",
            "size": "hero",
            "prompt": (
                "Technical visualization of Myers diff edit graph "
                "showing the shortest edit path between two sequences, "
                "dark developer algorithm editorial"
            ),
        },
        {
            "slug": "unified-diff-format-hero",
            "size": "hero",
            "prompt": (
                "Terminal or editor showing unified diff patch format "
                "with chunk headers and plus minus lines, dark monospace editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "utmbuilder.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/utmbuilder.io/public",
            "prompt": (
                "UTM-tagged URL with parameter labels overlaid — source medium campaign — "
                "clean marketing analytics tool editorial"
            ),
        },
        {
            "slug": "google-analytics-utm-hero",
            "size": "hero",
            "prompt": (
                "Google Analytics 4 acquisition report interface showing "
                "UTM campaign parameter data, marketing analytics editorial"
            ),
        },
        {
            "slug": "how-to-track-marketing-campaigns-hero",
            "size": "hero",
            "prompt": (
                "Marketing campaign tracking dashboard showing traffic sources "
                "by UTM parameters, clean analytics editorial"
            ),
        },
        {
            "slug": "utm-builder-guide-hero",
            "size": "hero",
            "prompt": (
                "UTM link builder form with source medium campaign fields filled in "
                "and a generated tagged URL output, clean marketing tool editorial"
            ),
        },
        {
            "slug": "utm-parameters-hero",
            "size": "hero",
            "prompt": (
                "UTM parameter breakdown diagram showing all five parameters — "
                "source medium campaign content term — with example values, "
                "clean marketing educational editorial"
            ),
        },
        {
            "slug": "utm-source-medium-campaign-hero",
            "size": "hero",
            "prompt": (
                "Three URL parameters highlighted side by side — utm_source "
                "utm_medium utm_campaign — with example values beneath each, "
                "clean marketing editorial"
            ),
        },
        {
            "slug": "utm-tracking-hero",
            "size": "hero",
            "prompt": (
                "Campaign performance bar chart showing traffic by UTM-tracked "
                "source channels, clean marketing analytics editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "uuidgen.io": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/uuidgen.io/public",
            "prompt": (
                "UUID string in monospace font prominently displayed on dark background, "
                "clean developer tool editorial, identifier concept"
            ),
        },
        {
            "slug": "generate-uuid-hero",
            "size": "hero",
            "prompt": (
                "Terminal showing UUID generation commands in Python JavaScript "
                "and CLI side by side, dark monospace developer editorial"
            ),
        },
        {
            "slug": "how-to-generate-uuid-code-hero",
            "size": "hero",
            "prompt": (
                "Code editor showing UUID generation code snippets in Python "
                "JavaScript Go and SQL with syntax highlighting, dark developer editorial"
            ),
        },
        {
            "slug": "uuid-in-database-hero",
            "size": "hero",
            "prompt": (
                "Database schema diagram showing a UUID primary key field "
                "with index indicator and example UUID value, dark developer editorial"
            ),
        },
        {
            "slug": "uuid-v4-vs-v7-hero",
            "size": "hero",
            "prompt": (
                "Side-by-side comparison of UUID v4 random format versus "
                "UUID v7 with timestamp prefix highlighted, dark monospace editorial"
            ),
        },
        {
            "slug": "uuid-vs-guid-hero",
            "size": "hero",
            "prompt": (
                "UUID and GUID strings displayed side by side showing "
                "their identical 8-4-4-4-12 hex format, dark monospace developer editorial"
            ),
        },
        {
            "slug": "what-is-a-uuid-hero",
            "size": "hero",
            "prompt": (
                "Single UUID string 550e8400-e29b-41d4-a716-446655440000 displayed in large "
                "monospace font with each segment labeled version node timestamp, "
                "dark terminal aesthetic developer educational editorial"
            ),
        },
    ],

    # -----------------------------------------------------------------------
    "wordcounttools.com": [
        {
            "slug": "og-default",
            "size": "hero",
            "output_dir_override": "sites/wordcounttools.com/public",
            "prompt": (
                "Clean word count tool interface showing word count character count "
                "and reading time statistics for a text, modern tool editorial"
            ),
        },
        {
            "slug": "average-words-per-page-hero",
            "size": "hero",
            "prompt": (
                "Page of printed text with word count annotation overlaid, "
                "showing counts for different document formats, editorial illustration"
            ),
        },
        {
            "slug": "character-count-guide-hero",
            "size": "hero",
            "prompt": (
                "Social media composer interfaces showing character count limits "
                "for different platforms, clean editorial tool screenshot style"
            ),
        },
        {
            "slug": "flesch-kincaid-readability-hero",
            "size": "hero",
            "prompt": (
                "Readability score gauge or meter showing text complexity rating "
                "with grade level indicator, clean educational editorial"
            ),
        },
        {
            "slug": "how-many-words-in-a-novel-hero",
            "size": "hero",
            "prompt": (
                "Stack of books by genre with word count labels beside each, "
                "clean editorial illustration, publishing concept"
            ),
        },
        {
            "slug": "reading-time-calculator-hero",
            "size": "hero",
            "prompt": (
                "Article preview with an estimated reading time badge overlaid, "
                "clock icon and minute count, clean editorial tool concept"
            ),
        },
        {
            "slug": "word-count-google-docs-hero",
            "size": "hero",
            "prompt": (
                "Google Docs interface showing the Word Count dialog box "
                "with statistics visible, clean editorial screenshot style"
            ),
        },
    ],
}

SITE_ORDER = [
    "caseconvert.io", "citefast.io", "crontab.io", "cssminify.io",
    "encodeonline.io", "gradientcss.io", "htmlformat.io", "jwtinspect.io",
    "passwordgen.io", "qrcodegen.io", "regexbuilder.io", "sqlformat.io",
    "textdiff.pro", "utmbuilder.io", "uuidgen.io", "wordcounttools.com",
]

BATCH_A = SITE_ORDER[:8]
BATCH_B = SITE_ORDER[8:]

# ---------------------------------------------------------------------------
# Pipeline (lazy-loaded)
# ---------------------------------------------------------------------------
_pipe = None


def get_pipeline():
    global _pipe
    if _pipe is None:
        os.environ.setdefault("PYTORCH_CUDA_ALLOC_CONF", "expandable_segments:True")
        print("Loading ERNIE-Image-Turbo...", file=sys.stderr)
        from diffusers import ErnieImagePipeline
        from diffusers.quantizers.pipe_quant_config import PipelineQuantizationConfig
        from transformers import AutoModel, AutoModelForCausalLM, BitsAndBytesConfig
        import torch
        import gc

        bnb_4bit = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
        )
        quant_config = PipelineQuantizationConfig(
            quant_backend="bitsandbytes_4bit",
            quant_kwargs={
                "load_in_4bit": True,
                "bnb_4bit_compute_dtype": torch.bfloat16,
                "bnb_4bit_use_double_quant": True,
            },
            components_to_quantize=["transformer"],
        )

        _pipe = ErnieImagePipeline.from_pretrained(
            "baidu/ERNIE-Image-Turbo",
            torch_dtype=torch.bfloat16,
            quantization_config=quant_config,
            cache_dir="/data/huggingface",
        )

        snap_dir = [
            d
            for d in os.listdir(
                "/data/huggingface/models--baidu--ERNIE-Image-Turbo/snapshots/"
            )
            if not d.startswith(".")
        ][0]
        snap_path = (
            f"/data/huggingface/models--baidu--ERNIE-Image-Turbo/snapshots/{snap_dir}"
        )

        del _pipe.text_encoder
        gc.collect()
        _pipe.text_encoder = AutoModel.from_pretrained(
            f"{snap_path}/text_encoder",
            quantization_config=bnb_4bit,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

        del _pipe.pe
        gc.collect()
        _pipe.pe = AutoModelForCausalLM.from_pretrained(
            f"{snap_path}/pe",
            quantization_config=bnb_4bit,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )

        _pipe.transformer = _pipe.transformer.to("cuda:0")
        _pipe.vae = _pipe.vae.to("cuda:0")
        print(
            f"Pipeline ready. GPU0: {torch.cuda.mem_get_info(0)[1]/1e9:.1f}GB, "
            f"GPU1: {torch.cuda.mem_get_info(1)[1]/1e9:.1f}GB",
            file=sys.stderr,
        )
    return _pipe


# ---------------------------------------------------------------------------
# Core generation
# ---------------------------------------------------------------------------
def center_crop_to_ratio(img: Image.Image, target_w: int, target_h: int) -> Image.Image:
    src_w, src_h = img.size
    target_ratio = target_w / target_h
    src_ratio = src_w / src_h
    if src_ratio > target_ratio:
        new_w = int(src_h * target_ratio)
        left = (src_w - new_w) // 2
        img = img.crop((left, 0, left + new_w, src_h))
    else:
        new_h = int(src_w / target_ratio)
        top = (src_h - new_h) // 2
        img = img.crop((0, top, src_w, top + new_h))
    return img.resize((target_w, target_h), Image.LANCZOS)


def generate_image(spec: dict, default_output_dir: str, skip_existing: bool = True) -> str:
    slug = spec["slug"]
    size_key = spec["size"]
    prompt = spec["prompt"]
    target_w, target_h = SIZES[size_key]

    output_dir = os.path.abspath(
        spec.get("output_dir_override", default_output_dir)
    )
    out_path = os.path.join(output_dir, f"{slug}.png")

    if skip_existing and os.path.exists(out_path):
        print(f"  [skip] {slug}.png", file=sys.stderr)
        return out_path

    pipe = get_pipeline()
    import torch

    seed_val = int(hashlib.md5(slug.encode()).hexdigest()[:8], 16)
    print(f"  [{slug}] Generating ({target_w}x{target_h})...", file=sys.stderr)
    t0 = time.time()
    torch.cuda.empty_cache()
    raw = pipe(
        prompt=prompt,
        height=1024,
        width=1024,
        num_inference_steps=8,
        generator=torch.Generator(device="cpu").manual_seed(seed_val),
    ).images[0]
    final = center_crop_to_ratio(raw, target_w, target_h)
    os.makedirs(output_dir, exist_ok=True)
    final.save(out_path, "PNG", optimize=True)
    elapsed = time.time() - t0
    print(f"  Saved {out_path} in {elapsed:.1f}s", file=sys.stderr)
    return out_path


def run_site(site: str, force: bool = False, test: bool = False):
    if site not in SITE_MANIFESTS:
        print(f"Unknown site: {site}", file=sys.stderr)
        sys.exit(1)
    specs = SITE_MANIFESTS[site]
    blog_output_dir = os.path.abspath(f"sites/{site}/public/images/blog")
    os.makedirs(blog_output_dir, exist_ok=True)
    if test:
        specs = [specs[0]]
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Site: {site} ({len(specs)} images)", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)
    for spec in specs:
        generate_image(spec, blog_output_dir, skip_existing=not force)


def run_batch(sites: list, force: bool = False):
    for site in sites:
        run_site(site, force=force)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate dev/tool hero images for 16 utility sites"
    )
    parser.add_argument("--site", choices=SITE_ORDER, help="Single site")
    parser.add_argument("--batch", choices=["a", "b"], help="Run batch a (sites 1-8) or b (sites 9-16)")
    parser.add_argument("--all-sites", action="store_true", help="All 16 sites")
    parser.add_argument("--all", action="store_true", help="All images for selected --site")
    parser.add_argument("--test", action="store_true", help="Test: OG only for selected site")
    parser.add_argument("--force", action="store_true", help="Overwrite existing")

    args = parser.parse_args()

    if args.all_sites:
        run_batch(SITE_ORDER, force=args.force)
    elif args.batch == "a":
        run_batch(BATCH_A, force=args.force)
    elif args.batch == "b":
        run_batch(BATCH_B, force=args.force)
    elif args.site:
        run_site(args.site, force=args.force, test=args.test)
    else:
        parser.print_help()
        sys.exit(0)


if __name__ == "__main__":
    main()
