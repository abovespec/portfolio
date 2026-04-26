#!/usr/bin/env python3
"""
AI blog image generator — INF-43 batch (22 remaining sites).

Generates hero (1200x630), img1 (600x400), img2 (1200x630) for every blog article
on 22 sites. All prompts are visual/atmospheric with no significant text content,
per board guidance from INF-42.

Usage:
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_inf43.py --site carleasecalc.com --all
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_inf43.py --site carleasecalc.com --test
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_inf43.py --all-sites
    /data/venvs/ai-image-gen/bin/python3.11 scripts/ai_generate_blog_images_inf43.py --all-sites --resume
"""

import argparse
import hashlib
import os
import sys
import time

from PIL import Image

SIZES = {
    "hero": (1200, 630),
    "img1": (600, 400),
    "img2": (1200, 630),
}

# ---------------------------------------------------------------------------
# Site manifests — all prompts visual/atmospheric, no text in images
# Each article gets 3 entries: slug-hero, slug-1, slug-2
# ---------------------------------------------------------------------------

SITE_MANIFESTS = {

    # =========================================================================
    "carleasecalc.com": [
        # car-depreciation-calculator-by-model-which-cars-hold-value-best
        {"slug": "car-depreciation-calculator-by-model-which-cars-hold-value-best-hero", "size": "hero",
         "prompt": "Row of new cars at a dealership lot under golden hour light, gleaming paint, wide parking area, warm atmospheric photography, no people, editorial automotive"},
        {"slug": "car-depreciation-calculator-by-model-which-cars-hold-value-best-1", "size": "img1",
         "prompt": "Close-up of a luxury car wheel and brake disc, polished chrome rim, editorial automotive detail, warm natural light"},
        {"slug": "car-depreciation-calculator-by-model-which-cars-hold-value-best-2", "size": "img2",
         "prompt": "Two cars side by side on a road, one vintage and one modern, depreciation concept, atmospheric editorial photography"},

        # lease-vs-buy-car-calculator-2025-total-cost-comparison
        {"slug": "lease-vs-buy-car-calculator-2025-total-cost-comparison-hero", "size": "hero",
         "prompt": "Car keys on one side and a pen on a contract on the other side of a clean desk, warm editorial still life, financial decision concept, no text"},
        {"slug": "lease-vs-buy-car-calculator-2025-total-cost-comparison-1", "size": "img1",
         "prompt": "Single car key fob resting on a wooden surface, warm natural light, clean product photography"},
        {"slug": "lease-vs-buy-car-calculator-2025-total-cost-comparison-2", "size": "img2",
         "prompt": "Modern car interior dashboard view, hands on steering wheel, sunlight through windshield, atmospheric driving concept"},

        # total-cost-of-car-ownership-calculator-the-real-monthly-number
        {"slug": "total-cost-of-car-ownership-calculator-the-real-monthly-number-hero", "size": "hero",
         "prompt": "Car parked at a gas station at dusk, warm golden pump lights, atmospheric photography, ownership cost concept"},
        {"slug": "total-cost-of-car-ownership-calculator-the-real-monthly-number-1", "size": "img1",
         "prompt": "Close-up of a car odometer and fuel gauge, warm dashboard glow, editorial automotive interior detail"},
        {"slug": "total-cost-of-car-ownership-calculator-the-real-monthly-number-2", "size": "img2",
         "prompt": "Car driving through a tunnel, light trails, long exposure, atmospheric editorial automotive photography"},

        # electric-car-total-cost-of-ownership-ev-vs-gas-in-2025
        {"slug": "electric-car-total-cost-of-ownership-ev-vs-gas-in-2025-hero", "size": "hero",
         "prompt": "Electric car plugged into a charging station in a modern parking garage, soft blue and white glow, EV concept editorial"},
        {"slug": "electric-car-total-cost-of-ownership-ev-vs-gas-in-2025-1", "size": "img1",
         "prompt": "Electric vehicle charging port closeup with green charging indicator light, clean editorial product photography"},
        {"slug": "electric-car-total-cost-of-ownership-ev-vs-gas-in-2025-2", "size": "img2",
         "prompt": "Modern electric car on an open highway at sunset, clean silhouette, atmospheric landscape editorial"},

        # is-it-better-to-lease-or-buy-a-car-decision-framework
        {"slug": "is-it-better-to-lease-or-buy-a-car-decision-framework-hero", "size": "hero",
         "prompt": "Fork in a road surrounded by green trees, decision choice concept, warm natural light aerial perspective, editorial landscape"},
        {"slug": "is-it-better-to-lease-or-buy-a-car-decision-framework-1", "size": "img1",
         "prompt": "Hand reaching toward a car door handle in a showroom, warm elegant lighting, automotive editorial"},
        {"slug": "is-it-better-to-lease-or-buy-a-car-decision-framework-2", "size": "img2",
         "prompt": "Car showroom interior with several vehicles displayed, warm professional lighting, upscale automotive photography"},

        # fuel-cost-calculator-for-road-trips-budget-your-gas-expenses
        {"slug": "fuel-cost-calculator-for-road-trips-budget-your-gas-expenses-hero", "size": "hero",
         "prompt": "Open road stretching into desert mountains at golden hour, road trip concept, warm atmospheric landscape photography"},
        {"slug": "fuel-cost-calculator-for-road-trips-budget-your-gas-expenses-1", "size": "img1",
         "prompt": "Close-up of a gas pump nozzle inserted in a car, warm afternoon light, editorial automotive detail"},
        {"slug": "fuel-cost-calculator-for-road-trips-budget-your-gas-expenses-2", "size": "img2",
         "prompt": "Car on a coastal highway, blue ocean on one side, cliffs on the other, road trip editorial landscape"},
    ],

    # =========================================================================
    "freeinvoicemake.com": [
        # invoice-template-for-small-business-free-and-professional
        {"slug": "invoice-template-for-small-business-free-and-professional-hero", "size": "hero",
         "prompt": "Clean modern office desk with a printed document, coffee cup, and pen, warm professional editorial photography, business concept, no readable text"},
        {"slug": "invoice-template-for-small-business-free-and-professional-1", "size": "img1",
         "prompt": "Stack of neatly organized papers and a pen on a white desk, warm editorial business still life"},
        {"slug": "invoice-template-for-small-business-free-and-professional-2", "size": "img2",
         "prompt": "Small business storefront with warm window light, professional editorial photography, business owner concept"},

        # free-invoice-generator-no-signup-create-and-print-in-seconds
        {"slug": "free-invoice-generator-no-signup-create-and-print-in-seconds-hero", "size": "hero",
         "prompt": "Modern laptop on a clean desk with a printer nearby, professional home office setup, warm editorial photography"},
        {"slug": "free-invoice-generator-no-signup-create-and-print-in-seconds-1", "size": "img1",
         "prompt": "Laptop with a document on screen, blurred background, warm desk editorial photography"},
        {"slug": "free-invoice-generator-no-signup-create-and-print-in-seconds-2", "size": "img2",
         "prompt": "Person at a laptop in a bright modern office, focused work concept, editorial natural light photography"},

        # how-to-write-an-invoice-for-freelance-work-a-step-by-step-guide
        {"slug": "how-to-write-an-invoice-for-freelance-work-a-step-by-step-guide-hero", "size": "hero",
         "prompt": "Freelancer working at a wooden desk with a laptop and notepad, warm home office atmosphere, editorial photography"},
        {"slug": "how-to-write-an-invoice-for-freelance-work-a-step-by-step-guide-1", "size": "img1",
         "prompt": "Close-up of a pen writing on paper at a desk, warm light, clean editorial still life"},
        {"slug": "how-to-write-an-invoice-for-freelance-work-a-step-by-step-guide-2", "size": "img2",
         "prompt": "Freelance workspace — laptop, coffee, sketchbook on a wooden table, warm natural window light"},

        # invoice-payment-terms-examples-net-30-due-on-receipt-and-more
        {"slug": "invoice-payment-terms-examples-net-30-due-on-receipt-and-more-hero", "size": "hero",
         "prompt": "Calendar with a date circled and a pen resting on it, payment deadline concept, warm editorial photography"},
        {"slug": "invoice-payment-terms-examples-net-30-due-on-receipt-and-more-1", "size": "img1",
         "prompt": "Close-up of a calendar page, soft focus, warm tones, time concept editorial"},
        {"slug": "invoice-payment-terms-examples-net-30-due-on-receipt-and-more-2", "size": "img2",
         "prompt": "Office desk with a document and a clock visible, professional deadline concept, editorial photography"},

        # how-to-start-invoicing-as-a-freelancer-from-first-client-to-payment
        {"slug": "how-to-start-invoicing-as-a-freelancer-from-first-client-to-payment-hero", "size": "hero",
         "prompt": "Excited freelancer at laptop in a bright cafe, first client concept, editorial natural light photography"},
        {"slug": "how-to-start-invoicing-as-a-freelancer-from-first-client-to-payment-1", "size": "img1",
         "prompt": "Hand shaking concept — two hands reaching toward each other, professional deal editorial, warm tones"},
        {"slug": "how-to-start-invoicing-as-a-freelancer-from-first-client-to-payment-2", "size": "img2",
         "prompt": "Smartphone showing a banking app with a successful payment notification, warm editorial product photography, no readable UI text"},

        # best-free-invoicing-software-2025-top-picks-for-freelancers-and-small-business
        {"slug": "best-free-invoicing-software-2025-top-picks-for-freelancers-and-small-business-hero", "size": "hero",
         "prompt": "Multiple devices — laptop, tablet, phone — on a clean desk showing work tools, warm editorial tech photography"},
        {"slug": "best-free-invoicing-software-2025-top-picks-for-freelancers-and-small-business-1", "size": "img1",
         "prompt": "Tablet and stylus on a modern desk, blurred background, warm professional editorial"},
        {"slug": "best-free-invoicing-software-2025-top-picks-for-freelancers-and-small-business-2", "size": "img2",
         "prompt": "Small business owner at a bright desk with multiple screens, focused work atmosphere, editorial photography"},
    ],

    # =========================================================================
    "gradecalc.io": [
        # what-grade-do-i-need-on-my-final-exam-calculator
        {"slug": "what-grade-do-i-need-on-my-final-exam-calculator-hero", "size": "hero",
         "prompt": "Student studying at a library desk with open textbooks and notes under warm lamp light, exam preparation concept"},
        {"slug": "what-grade-do-i-need-on-my-final-exam-calculator-1", "size": "img1",
         "prompt": "Close-up of a student writing in a notebook, pencil in hand, warm desk light, editorial study detail"},
        {"slug": "what-grade-do-i-need-on-my-final-exam-calculator-2", "size": "img2",
         "prompt": "Empty exam classroom with rows of desks, morning light through windows, academic atmosphere"},

        # how-to-calculate-weighted-gpa-honors-ap-and-ib-explained
        {"slug": "how-to-calculate-weighted-gpa-honors-ap-and-ib-explained-hero", "size": "hero",
         "prompt": "Stack of advanced textbooks on a university campus bench, autumn leaves, warm academic atmosphere"},
        {"slug": "how-to-calculate-weighted-gpa-honors-ap-and-ib-explained-1", "size": "img1",
         "prompt": "Academic certificate or diploma leaning against a stack of books, warm editorial still life"},
        {"slug": "how-to-calculate-weighted-gpa-honors-ap-and-ib-explained-2", "size": "img2",
         "prompt": "University lecture hall with empty seats, warm natural light through tall windows, academic editorial"},

        # final-exam-grade-calculator-predict-your-course-grade
        {"slug": "final-exam-grade-calculator-predict-your-course-grade-hero", "size": "hero",
         "prompt": "Student with a laptop and papers at a coffee shop, focused study session, warm ambient lighting editorial"},
        {"slug": "final-exam-grade-calculator-predict-your-course-grade-1", "size": "img1",
         "prompt": "Pencil and eraser on a blank exam paper, clean editorial still life, warm tones"},
        {"slug": "final-exam-grade-calculator-predict-your-course-grade-2", "size": "img2",
         "prompt": "Scattered study materials — notes, highlighters, textbooks — on a student desk, end-of-semester atmosphere"},

        # study-schedule-generator-for-exams-plan-your-revision
        {"slug": "study-schedule-generator-for-exams-plan-your-revision-hero", "size": "hero",
         "prompt": "Monthly planner open on a desk with a pen and colorful sticky notes, organized study planning concept"},
        {"slug": "study-schedule-generator-for-exams-plan-your-revision-1", "size": "img1",
         "prompt": "Close-up of a weekly planner with colorful highlights, clean editorial flat lay"},
        {"slug": "study-schedule-generator-for-exams-plan-your-revision-2", "size": "img2",
         "prompt": "Student pinning a schedule to a cork board, warm home study editorial photography"},

        # how-to-get-a-4-0-gpa-in-college-strategies-that-work
        {"slug": "how-to-get-a-4-0-gpa-in-college-strategies-that-work-hero", "size": "hero",
         "prompt": "College campus pathway in autumn with golden trees and students in the distance, academic achievement atmosphere"},
        {"slug": "how-to-get-a-4-0-gpa-in-college-strategies-that-work-1", "size": "img1",
         "prompt": "Student sitting under a tree on campus with an open book, warm afternoon editorial photography"},
        {"slug": "how-to-get-a-4-0-gpa-in-college-strategies-that-work-2", "size": "img2",
         "prompt": "University library interior with tall bookshelves and warm study lamps, academic achievement editorial"},

        # gpa-calculator-with-ap-classes-weighted-and-unweighted
        {"slug": "gpa-calculator-with-ap-classes-weighted-and-unweighted-hero", "size": "hero",
         "prompt": "AP and honors textbooks stacked on a school locker shelf, warm editorial academic still life"},
        {"slug": "gpa-calculator-with-ap-classes-weighted-and-unweighted-1", "size": "img1",
         "prompt": "Close-up of a gradebook or report card, blurred, warm editorial, academic concept"},
        {"slug": "gpa-calculator-with-ap-classes-weighted-and-unweighted-2", "size": "img2",
         "prompt": "Student presenting a project to a class, academic atmosphere, warm editorial photography"},
    ],

    # =========================================================================
    "isitdown.fyi": [
        # website-status-page-best-practices-build-trust-during-outages
        {"slug": "website-status-page-best-practices-build-trust-during-outages-hero", "size": "hero",
         "prompt": "Server room with blinking status lights in blue and green, infrastructure monitoring concept, atmospheric tech photography"},
        {"slug": "website-status-page-best-practices-build-trust-during-outages-1", "size": "img1",
         "prompt": "Close-up of server rack LED status indicators, green and amber lights, dramatic dark background"},
        {"slug": "website-status-page-best-practices-build-trust-during-outages-2", "size": "img2",
         "prompt": "Data center corridor with glowing server racks receding into the distance, blue atmospheric light"},

        # is-github-down-right-now-how-to-check-and-verify
        {"slug": "is-github-down-right-now-how-to-check-and-verify-hero", "size": "hero",
         "prompt": "Developer at a laptop with an error screen glow on their face in a dark office, connectivity issue concept, moody editorial"},
        {"slug": "is-github-down-right-now-how-to-check-and-verify-1", "size": "img1",
         "prompt": "Screen showing a connection error symbol — spinning wheel or broken chain icon, blurred background, dark moody editorial"},
        {"slug": "is-github-down-right-now-how-to-check-and-verify-2", "size": "img2",
         "prompt": "Developer looking pensively at multiple monitors in a dark room, troubleshooting atmosphere, editorial photography"},

        # free-website-downtime-checker-monitor-uptime-without-paying
        {"slug": "free-website-downtime-checker-monitor-uptime-without-paying-hero", "size": "hero",
         "prompt": "Dashboard with multiple monitors showing system uptime graphs, green lines, professional tech editorial"},
        {"slug": "free-website-downtime-checker-monitor-uptime-without-paying-1", "size": "img1",
         "prompt": "Close-up of a network monitoring display with pulse graphs, dark background, green uptime glow"},
        {"slug": "free-website-downtime-checker-monitor-uptime-without-paying-2", "size": "img2",
         "prompt": "Network operations center with multiple screens, people monitoring systems in background, professional editorial"},

        # dns-probe-finished-nxdomain-fix-step-by-step-solutions
        {"slug": "dns-probe-finished-nxdomain-fix-step-by-step-solutions-hero", "size": "hero",
         "prompt": "Tangled ethernet cables and a blinking router, DNS and network concept, moody dark editorial photography"},
        {"slug": "dns-probe-finished-nxdomain-fix-step-by-step-solutions-1", "size": "img1",
         "prompt": "Close-up of an ethernet cable being plugged into a router, warm editorial detail, network connection concept"},
        {"slug": "dns-probe-finished-nxdomain-fix-step-by-step-solutions-2", "size": "img2",
         "prompt": "Home router with blinking lights in a dark room, atmospheric connectivity editorial"},

        # how-to-check-if-a-website-is-down-5-methods-that-work
        {"slug": "how-to-check-if-a-website-is-down-5-methods-that-work-hero", "size": "hero",
         "prompt": "Person on a laptop in a cafe, screen reflecting a loading animation, website checking concept, warm editorial"},
        {"slug": "how-to-check-if-a-website-is-down-5-methods-that-work-1", "size": "img1",
         "prompt": "Laptop screen with an hourglass loading indicator, blurred office background, editorial tech concept"},
        {"slug": "how-to-check-if-a-website-is-down-5-methods-that-work-2", "size": "img2",
         "prompt": "Multiple people checking phones and laptops simultaneously in a public space, connectivity checking atmosphere"},

        # best-free-website-monitoring-tools-compared-2025
        {"slug": "best-free-website-monitoring-tools-compared-2025-hero", "size": "hero",
         "prompt": "Multiple laptops and tablets arranged on a table showing different monitoring interfaces, warm tech editorial"},
        {"slug": "best-free-website-monitoring-tools-compared-2025-1", "size": "img1",
         "prompt": "Tablet displaying a dashboard with health metrics visualization, blurred office background, editorial"},
        {"slug": "best-free-website-monitoring-tools-compared-2025-2", "size": "img2",
         "prompt": "Tech setup with multiple monitors and plants in a modern home office, website monitoring work environment"},
    ],

    # =========================================================================
    "myfreelancerate.com": [
        # how-much-should-i-charge-as-a-freelancer-a-pricing-framework
        {"slug": "how-much-should-i-charge-as-a-freelancer-a-pricing-framework-hero", "size": "hero",
         "prompt": "Freelancer at a bright home office desk thinking, warm natural light, professional editorial photography"},
        {"slug": "how-much-should-i-charge-as-a-freelancer-a-pricing-framework-1", "size": "img1",
         "prompt": "Stack of coins arranged by height, pricing concept, warm editorial still life, gold tones"},
        {"slug": "how-much-should-i-charge-as-a-freelancer-a-pricing-framework-2", "size": "img2",
         "prompt": "Confident freelancer presenting work on a laptop to a client, professional meeting atmosphere"},

        # freelance-hourly-rate-calculator-by-industry-what-to-charge-in-2025
        {"slug": "freelance-hourly-rate-calculator-by-industry-what-to-charge-in-2025-hero", "size": "hero",
         "prompt": "Desk clock beside a laptop and notebook in a warm home studio, time equals money concept, editorial photography"},
        {"slug": "freelance-hourly-rate-calculator-by-industry-what-to-charge-in-2025-1", "size": "img1",
         "prompt": "Close-up of a clock face, blurred background, time value concept, editorial product photography"},
        {"slug": "freelance-hourly-rate-calculator-by-industry-what-to-charge-in-2025-2", "size": "img2",
         "prompt": "Freelancer working at a standing desk in a modern studio, warm afternoon light, productive atmosphere"},

        # project-based-pricing-formula-how-to-quote-fixed-price-work
        {"slug": "project-based-pricing-formula-how-to-quote-fixed-price-work-hero", "size": "hero",
         "prompt": "Blueprint or project plan spread on a desk with a ruler and pencil, project scope concept, warm editorial"},
        {"slug": "project-based-pricing-formula-how-to-quote-fixed-price-work-1", "size": "img1",
         "prompt": "Hands measuring with a ruler on architectural drawings, project planning close-up editorial"},
        {"slug": "project-based-pricing-formula-how-to-quote-fixed-price-work-2", "size": "img2",
         "prompt": "Client and freelancer discussing a project proposal, documents between them, professional meeting editorial"},

        # freelance-income-goal-calculator-set-and-hit-your-target-earnings
        {"slug": "freelance-income-goal-calculator-set-and-hit-your-target-earnings-hero", "size": "hero",
         "prompt": "Target on a dartboard with a dart hitting the bullseye, goal achievement concept, clean editorial photography"},
        {"slug": "freelance-income-goal-calculator-set-and-hit-your-target-earnings-1", "size": "img1",
         "prompt": "Close-up of dart in bullseye, red and white target, success concept editorial"},
        {"slug": "freelance-income-goal-calculator-set-and-hit-your-target-earnings-2", "size": "img2",
         "prompt": "Person celebrating with arms raised at a desk after achieving a milestone, warm editorial photography"},

        # how-to-negotiate-freelance-rates-without-losing-the-client
        {"slug": "how-to-negotiate-freelance-rates-without-losing-the-client-hero", "size": "hero",
         "prompt": "Two people in a professional negotiation meeting, documents on table, warm editorial business photography"},
        {"slug": "how-to-negotiate-freelance-rates-without-losing-the-client-1", "size": "img1",
         "prompt": "Two hands reaching toward each other across a table, handshake approaching, deal concept editorial"},
        {"slug": "how-to-negotiate-freelance-rates-without-losing-the-client-2", "size": "img2",
         "prompt": "Coffee meeting between two professionals at a bright cafe, collaborative discussion atmosphere"},

        # value-based-pricing-for-freelancers-charge-for-outcomes-not-hours
        {"slug": "value-based-pricing-for-freelancers-charge-for-outcomes-not-hours-hero", "size": "hero",
         "prompt": "Premium product displayed in a luxury setting, value and quality concept, elegant editorial photography"},
        {"slug": "value-based-pricing-for-freelancers-charge-for-outcomes-not-hours-1", "size": "img1",
         "prompt": "Single high-quality product on a pedestal with dramatic lighting, premium value concept"},
        {"slug": "value-based-pricing-for-freelancers-charge-for-outcomes-not-hours-2", "size": "img2",
         "prompt": "Satisfied client viewing completed deliverable on a screen, positive outcome atmosphere, editorial"},
    ],

    # =========================================================================
    "paintcalc.io": [
        # how-much-paint-do-i-need-for-a-12x12-room-exact-calculation
        {"slug": "how-much-paint-do-i-need-for-a-12x12-room-exact-calculation-hero", "size": "hero",
         "prompt": "Empty room being freshly painted, roller brushes, paint cans, natural light through a window, home renovation concept"},
        {"slug": "how-much-paint-do-i-need-for-a-12x12-room-exact-calculation-1", "size": "img1",
         "prompt": "Close-up of a paint roller applying color to a wall, warm editorial detail, renovation concept"},
        {"slug": "how-much-paint-do-i-need-for-a-12x12-room-exact-calculation-2", "size": "img2",
         "prompt": "Freshly painted living room with warm tones, natural light, beautiful home renovation result"},

        # hvac-btu-calculator-by-room-size-sizing-guide-for-ac-and-heat
        {"slug": "hvac-btu-calculator-by-room-size-sizing-guide-for-ac-and-heat-hero", "size": "hero",
         "prompt": "Modern HVAC unit installed on an exterior wall, blue sky background, clean product photography"},
        {"slug": "hvac-btu-calculator-by-room-size-sizing-guide-for-ac-and-heat-1", "size": "img1",
         "prompt": "Indoor air conditioning vent in a ceiling, clean white room, cool air concept editorial"},
        {"slug": "hvac-btu-calculator-by-room-size-sizing-guide-for-ac-and-heat-2", "size": "img2",
         "prompt": "Person adjusting a smart thermostat on a wall, home comfort concept, warm editorial photography"},

        # paint-calculator-by-square-feet-coverage-coats-and-cost
        {"slug": "paint-calculator-by-square-feet-coverage-coats-and-cost-hero", "size": "hero",
         "prompt": "Paint swatches and color samples spread on a floor, interior design planning concept, editorial overhead shot"},
        {"slug": "paint-calculator-by-square-feet-coverage-coats-and-cost-1", "size": "img1",
         "prompt": "Close-up of paint color swatches fanned out, warm natural light, editorial design detail"},
        {"slug": "paint-calculator-by-square-feet-coverage-coats-and-cost-2", "size": "img2",
         "prompt": "Interior designer holding color swatches against a wall, home design planning atmosphere"},

        # roofing-square-footage-calculator-shingles-bundles-and-cost
        {"slug": "roofing-square-footage-calculator-shingles-bundles-and-cost-hero", "size": "hero",
         "prompt": "Roofer working on a house roof on a sunny day, stacked shingles, construction concept editorial"},
        {"slug": "roofing-square-footage-calculator-shingles-bundles-and-cost-1", "size": "img1",
         "prompt": "Close-up of roof shingles being laid, texture and pattern detail, construction editorial"},
        {"slug": "roofing-square-footage-calculator-shingles-bundles-and-cost-2", "size": "img2",
         "prompt": "Wide aerial view of a residential rooftop, warm afternoon sun, home improvement concept"},

        # roof-replacement-cost-estimator-2025-pricing-by-material-and-size
        {"slug": "roof-replacement-cost-estimator-2025-pricing-by-material-and-size-hero", "size": "hero",
         "prompt": "Contractor reviewing a house exterior with a clipboard, home assessment concept, warm editorial photography"},
        {"slug": "roof-replacement-cost-estimator-2025-pricing-by-material-and-size-1", "size": "img1",
         "prompt": "Different roofing material samples arranged side by side, shingles and metal, construction editorial"},
        {"slug": "roof-replacement-cost-estimator-2025-pricing-by-material-and-size-2", "size": "img2",
         "prompt": "Construction crew working on a roof replacement, blue sky, progress concept editorial"},

        # flooring-cost-calculator-by-square-foot-material-and-installation
        {"slug": "flooring-cost-calculator-by-square-foot-material-and-installation-hero", "size": "hero",
         "prompt": "New hardwood flooring being installed in a bright empty room, home renovation editorial photography"},
        {"slug": "flooring-cost-calculator-by-square-foot-material-and-installation-1", "size": "img1",
         "prompt": "Close-up of hardwood floor planks, warm wood grain texture, editorial detail photography"},
        {"slug": "flooring-cost-calculator-by-square-foot-material-and-installation-2", "size": "img2",
         "prompt": "Various flooring material samples arranged on a surface, wood, tile, and vinyl options, editorial overhead"},
    ],

    # =========================================================================
    "pickthestack.com": [
        # best-free-scheduling-software-for-small-business-in-2025
        {"slug": "best-free-scheduling-software-for-small-business-in-2025-hero", "size": "hero",
         "prompt": "Clean modern home office with multiple devices — laptop, tablet, phone — organized workspace, tech editorial photography"},
        {"slug": "best-free-scheduling-software-for-small-business-in-2025-1", "size": "img1",
         "prompt": "Calendar application interface blurred on a tablet screen, scheduling concept, warm editorial"},
        {"slug": "best-free-scheduling-software-for-small-business-in-2025-2", "size": "img2",
         "prompt": "Small business team looking at a screen in a bright meeting room, collaborative scheduling atmosphere"},

        # calendly-vs-cal-com-pricing-2025-which-scheduling-tool-wins
        {"slug": "calendly-vs-cal-com-pricing-2025-which-scheduling-tool-wins-hero", "size": "hero",
         "prompt": "Two laptops side by side on a table with different interfaces glowing, comparison concept, moody editorial"},
        {"slug": "calendly-vs-cal-com-pricing-2025-which-scheduling-tool-wins-1", "size": "img1",
         "prompt": "Close-up of two devices next to each other, screens glowing, comparison concept editorial"},
        {"slug": "calendly-vs-cal-com-pricing-2025-which-scheduling-tool-wins-2", "size": "img2",
         "prompt": "Person switching between apps on a laptop, tool evaluation atmosphere, warm editorial photography"},

        # how-to-choose-scheduling-software-a-buyers-checklist
        {"slug": "how-to-choose-scheduling-software-a-buyers-checklist-hero", "size": "hero",
         "prompt": "Checklist on a clipboard beside a laptop and coffee, decision-making concept, warm editorial still life"},
        {"slug": "how-to-choose-scheduling-software-a-buyers-checklist-1", "size": "img1",
         "prompt": "Hand holding a pen checking items on a list, blurred background, decision concept editorial"},
        {"slug": "how-to-choose-scheduling-software-a-buyers-checklist-2", "size": "img2",
         "prompt": "Person researching software options on a laptop in a bright office, buyer evaluation atmosphere"},

        # best-saas-alternatives-to-popular-tools-the-2025-replacement-guide
        {"slug": "best-saas-alternatives-to-popular-tools-the-2025-replacement-guide-hero", "size": "hero",
         "prompt": "Multiple app icons on a tablet screen, blurred colorful grid, SaaS ecosystem concept, editorial tech photography"},
        {"slug": "best-saas-alternatives-to-popular-tools-the-2025-replacement-guide-1", "size": "img1",
         "prompt": "Tablet showing colorful app grid, blurred icons, software alternatives concept, warm editorial"},
        {"slug": "best-saas-alternatives-to-popular-tools-the-2025-replacement-guide-2", "size": "img2",
         "prompt": "Developer exploring a new tool on a laptop in a modern workspace, software discovery atmosphere"},

        # software-buying-guide-for-startups-build-your-stack-without-overspending
        {"slug": "software-buying-guide-for-startups-build-your-stack-without-overspending-hero", "size": "hero",
         "prompt": "Startup team in a bright open office space with laptops and whiteboards, collaborative tech atmosphere"},
        {"slug": "software-buying-guide-for-startups-build-your-stack-without-overspending-1", "size": "img1",
         "prompt": "Budget envelope and a USB drive, startup frugality concept, clean editorial still life"},
        {"slug": "software-buying-guide-for-startups-build-your-stack-without-overspending-2", "size": "img2",
         "prompt": "Founders planning their tech stack on a whiteboard, collaborative startup atmosphere, editorial"},

        # open-source-calendly-alternative-self-hosted-scheduling-in-2025
        {"slug": "open-source-calendly-alternative-self-hosted-scheduling-in-2025-hero", "size": "hero",
         "prompt": "Home server rack in a clean office closet, self-hosted infrastructure concept, editorial tech photography"},
        {"slug": "open-source-calendly-alternative-self-hosted-scheduling-in-2025-1", "size": "img1",
         "prompt": "Close-up of a Raspberry Pi or small server board, DIY tech concept, editorial product photography"},
        {"slug": "open-source-calendly-alternative-self-hosted-scheduling-in-2025-2", "size": "img2",
         "prompt": "Developer at a terminal in a dark room, self-hosting code, atmospheric tech editorial"},
    ],

    # =========================================================================
    "recipescale.io": [
        # meal-plan-generator-for-weight-loss-create-a-calorie-deficit-menu
        {"slug": "meal-plan-generator-for-weight-loss-create-a-calorie-deficit-menu-hero", "size": "hero",
         "prompt": "Healthy meal prep containers arranged neatly on a table, colorful vegetables and grains, food editorial photography"},
        {"slug": "meal-plan-generator-for-weight-loss-create-a-calorie-deficit-menu-1", "size": "img1",
         "prompt": "Close-up of a healthy salad bowl with colorful vegetables, warm food editorial photography"},
        {"slug": "meal-plan-generator-for-weight-loss-create-a-calorie-deficit-menu-2", "size": "img2",
         "prompt": "Weekly meal prep spread on a kitchen counter, healthy containers, planning concept editorial"},

        # macro-meal-planner-free-tool-for-balanced-nutrition
        {"slug": "macro-meal-planner-free-tool-for-balanced-nutrition-hero", "size": "hero",
         "prompt": "Balanced meal plate with protein, carbs, and vegetables, nutritional balance concept, beautiful food editorial"},
        {"slug": "macro-meal-planner-free-tool-for-balanced-nutrition-1", "size": "img1",
         "prompt": "Colorful fresh ingredients on a cutting board, macro nutrition concept, warm food editorial"},
        {"slug": "macro-meal-planner-free-tool-for-balanced-nutrition-2", "size": "img2",
         "prompt": "Nutrition-focused grocery shopping, fresh produce and lean proteins in a cart, editorial photography"},

        # how-to-double-a-recipe-calculator-tips-and-common-mistakes
        {"slug": "how-to-double-a-recipe-calculator-tips-and-common-mistakes-hero", "size": "hero",
         "prompt": "Two identical bowls of dough side by side on a kitchen counter, recipe doubling concept, warm baking editorial"},
        {"slug": "how-to-double-a-recipe-calculator-tips-and-common-mistakes-1", "size": "img1",
         "prompt": "Measuring cups and spoons arranged on a wooden counter, baking precision concept, warm editorial"},
        {"slug": "how-to-double-a-recipe-calculator-tips-and-common-mistakes-2", "size": "img2",
         "prompt": "Baker measuring and scaling ingredients carefully in a kitchen, recipe scaling atmosphere"},

        # recipe-scaler-calculator-convert-any-recipe-to-any-serving-size
        {"slug": "recipe-scaler-calculator-convert-any-recipe-to-any-serving-size-hero", "size": "hero",
         "prompt": "Multiple serving plates arranged on a dining table, dinner party scaling concept, warm atmospheric food editorial"},
        {"slug": "recipe-scaler-calculator-convert-any-recipe-to-any-serving-size-1", "size": "img1",
         "prompt": "Kitchen scale with food on it, measurement concept, warm food editorial photography"},
        {"slug": "recipe-scaler-calculator-convert-any-recipe-to-any-serving-size-2", "size": "img2",
         "prompt": "Large pot of soup on a stove with smaller portions being served, scaling up recipes concept"},

        # food-substitution-chart-for-baking-swaps-that-actually-work
        {"slug": "food-substitution-chart-for-baking-swaps-that-actually-work-hero", "size": "hero",
         "prompt": "Baking ingredients spread on a wooden table — flour, eggs, butter, alternatives — warm editorial still life"},
        {"slug": "food-substitution-chart-for-baking-swaps-that-actually-work-1", "size": "img1",
         "prompt": "Close-up of flaxseed and an egg, ingredient substitution concept, warm editorial detail"},
        {"slug": "food-substitution-chart-for-baking-swaps-that-actually-work-2", "size": "img2",
         "prompt": "Baker experimenting with alternative ingredients in a bright kitchen, creative baking atmosphere"},

        # nutrition-calculator-by-ingredient-build-recipes-with-confidence
        {"slug": "nutrition-calculator-by-ingredient-build-recipes-with-confidence-hero", "size": "hero",
         "prompt": "Fresh colorful ingredients laid out on a clean white counter, nutrition and cooking concept, editorial overhead"},
        {"slug": "nutrition-calculator-by-ingredient-build-recipes-with-confidence-1", "size": "img1",
         "prompt": "Vibrant fruits and vegetables close-up, nutrition abundance concept, warm food editorial"},
        {"slug": "nutrition-calculator-by-ingredient-build-recipes-with-confidence-2", "size": "img2",
         "prompt": "Chef carefully measuring ingredients into a recipe, confident cooking atmosphere, editorial photography"},
    ],

    # =========================================================================
    "rentalyieldcalc.com": [
        # cap-rate-calculator-by-zip-code-measure-property-performance
        {"slug": "cap-rate-calculator-by-zip-code-measure-property-performance-hero", "size": "hero",
         "prompt": "Aerial view of a residential neighborhood with houses and green lawns, real estate concept, warm editorial"},
        {"slug": "cap-rate-calculator-by-zip-code-measure-property-performance-1", "size": "img1",
         "prompt": "Close-up of a street sign at a intersection, neighborhood location concept, editorial photography"},
        {"slug": "cap-rate-calculator-by-zip-code-measure-property-performance-2", "size": "img2",
         "prompt": "City skyline with residential and commercial properties, real estate market overview editorial"},

        # rental-property-roi-calculator-total-return-on-investment
        {"slug": "rental-property-roi-calculator-total-return-on-investment-hero", "size": "hero",
         "prompt": "Investment property with a for-rent sign in front, warm neighborhood photography, real estate concept"},
        {"slug": "rental-property-roi-calculator-total-return-on-investment-1", "size": "img1",
         "prompt": "Stack of coins growing beside a small house model, return on investment concept, warm editorial"},
        {"slug": "rental-property-roi-calculator-total-return-on-investment-2", "size": "img2",
         "prompt": "Rental property keys on a table with financial documents, investor concept editorial photography"},

        # what-is-a-good-rental-yield-in-2025-benchmarks-by-market
        {"slug": "what-is-a-good-rental-yield-in-2025-benchmarks-by-market-hero", "size": "hero",
         "prompt": "Upscale residential street with well-maintained homes, high yield property concept, warm editorial photography"},
        {"slug": "what-is-a-good-rental-yield-in-2025-benchmarks-by-market-1", "size": "img1",
         "prompt": "House facade with a bright exterior and neat garden, attractive rental property editorial"},
        {"slug": "what-is-a-good-rental-yield-in-2025-benchmarks-by-market-2", "size": "img2",
         "prompt": "Real estate agent and investor viewing a property exterior, yield assessment concept editorial"},

        # rental-yield-calculator-by-postcode-find-high-yield-areas
        {"slug": "rental-yield-calculator-by-postcode-find-high-yield-areas-hero", "size": "hero",
         "prompt": "Map view of a city with highlighted neighborhoods, location research concept, warm editorial overhead"},
        {"slug": "rental-yield-calculator-by-postcode-find-high-yield-areas-1", "size": "img1",
         "prompt": "Real estate map pinned on a board with colorful markers, location research concept editorial"},
        {"slug": "rental-yield-calculator-by-postcode-find-high-yield-areas-2", "size": "img2",
         "prompt": "Investor walking through a promising neighborhood, property scouting atmosphere editorial"},

        # fix-and-flip-profit-calculator-estimate-your-next-deal-accurately
        {"slug": "fix-and-flip-profit-calculator-estimate-your-next-deal-accurately-hero", "size": "hero",
         "prompt": "Before and after — old house being renovated, scaffolding visible, transformation concept editorial"},
        {"slug": "fix-and-flip-profit-calculator-estimate-your-next-deal-accurately-1", "size": "img1",
         "prompt": "Contractor reviewing renovation progress inside a gutted house, fix and flip concept editorial"},
        {"slug": "fix-and-flip-profit-calculator-estimate-your-next-deal-accurately-2", "size": "img2",
         "prompt": "Renovated house with fresh paint and new landscaping, successful flip result editorial"},

        # cash-flow-positive-rental-property-how-to-find-and-verify-one
        {"slug": "cash-flow-positive-rental-property-how-to-find-and-verify-one-hero", "size": "hero",
         "prompt": "Rental property mailbox full, tenants visible in background through window, cash flow income concept"},
        {"slug": "cash-flow-positive-rental-property-how-to-find-and-verify-one-1", "size": "img1",
         "prompt": "Close-up of a rental lease document and a pen, property management editorial still life"},
        {"slug": "cash-flow-positive-rental-property-how-to-find-and-verify-one-2", "size": "img2",
         "prompt": "Happy property investor standing outside a well-maintained rental home, positive cash flow atmosphere"},
    ],

    # =========================================================================
    "rentwatch.io": [
        # salary-comparison-by-city-what-your-pay-is-really-worth
        {"slug": "salary-comparison-by-city-what-your-pay-is-really-worth-hero", "size": "hero",
         "prompt": "Skylines of two different cities side by side, urban comparison concept, dramatic editorial cityscape photography"},
        {"slug": "salary-comparison-by-city-what-your-pay-is-really-worth-1", "size": "img1",
         "prompt": "City street at golden hour with people walking, urban life concept, atmospheric editorial photography"},
        {"slug": "salary-comparison-by-city-what-your-pay-is-really-worth-2", "size": "img2",
         "prompt": "Person looking at two different city viewpoints, cost of living comparison atmosphere editorial"},

        # how-much-rent-can-i-afford-calculator-and-rule-of-thumb
        {"slug": "how-much-rent-can-i-afford-calculator-and-rule-of-thumb-hero", "size": "hero",
         "prompt": "Modern apartment building exterior in warm late afternoon light, urban housing concept editorial"},
        {"slug": "how-much-rent-can-i-afford-calculator-and-rule-of-thumb-1", "size": "img1",
         "prompt": "Apartment mailboxes in a building lobby, rental concept editorial, warm lighting"},
        {"slug": "how-much-rent-can-i-afford-calculator-and-rule-of-thumb-2", "size": "img2",
         "prompt": "Young professional looking at apartment listings on a laptop in a bright room, renter atmosphere"},

        # average-rent-by-city-2025-top-markets-ranked
        {"slug": "average-rent-by-city-2025-top-markets-ranked-hero", "size": "hero",
         "prompt": "Panoramic city skyline with diverse residential buildings, rent market overview concept, warm editorial"},
        {"slug": "average-rent-by-city-2025-top-markets-ranked-1", "size": "img1",
         "prompt": "Urban apartment windows at night, warm lights inside, city living concept editorial"},
        {"slug": "average-rent-by-city-2025-top-markets-ranked-2", "size": "img2",
         "prompt": "Aerial view of a major US city with residential and commercial buildings, rental market editorial"},

        # cost-of-living-comparison-by-city-salary-vs-expenses
        {"slug": "cost-of-living-comparison-by-city-salary-vs-expenses-hero", "size": "hero",
         "prompt": "Grocery store aisles with price tags visible but blurred, cost of living concept editorial"},
        {"slug": "cost-of-living-comparison-by-city-salary-vs-expenses-1", "size": "img1",
         "prompt": "Cart full of groceries, weekly expense concept, warm editorial food shopping photography"},
        {"slug": "cost-of-living-comparison-by-city-salary-vs-expenses-2", "size": "img2",
         "prompt": "Rent receipt and utility bills on a table, monthly expenses concept, warm editorial still life"},

        # rent-vs-buy-calculator-by-city-where-ownership-pays-off
        {"slug": "rent-vs-buy-calculator-by-city-where-ownership-pays-off-hero", "size": "hero",
         "prompt": "Apartment building next to a single-family home on a sunny street, rent vs buy comparison concept"},
        {"slug": "rent-vs-buy-calculator-by-city-where-ownership-pays-off-1", "size": "img1",
         "prompt": "House keys and a lease document side by side, rent vs buy decision concept editorial"},
        {"slug": "rent-vs-buy-calculator-by-city-where-ownership-pays-off-2", "size": "img2",
         "prompt": "New homeowners unlocking their front door, homeownership achievement concept editorial photography"},

        # cheapest-cities-to-rent-in-2025-affordable-housing-markets
        {"slug": "cheapest-cities-to-rent-in-2025-affordable-housing-markets-hero", "size": "hero",
         "prompt": "Affordable charming neighborhood with colorful small houses, budget housing concept, warm editorial"},
        {"slug": "cheapest-cities-to-rent-in-2025-affordable-housing-markets-1", "size": "img1",
         "prompt": "Cozy affordable apartment exterior with garden, budget living concept, warm editorial photography"},
        {"slug": "cheapest-cities-to-rent-in-2025-affordable-housing-markets-2", "size": "img2",
         "prompt": "Mid-size American city downtown at dusk, affordable urban living concept, atmospheric editorial"},
    ],

    # =========================================================================
    "sellerprofit.io": [
        # how-much-does-amazon-fba-cost-per-item-a-complete-breakdown
        {"slug": "how-much-does-amazon-fba-cost-per-item-a-complete-breakdown-hero", "size": "hero",
         "prompt": "Large warehouse with rows of shelves and products, fulfillment center concept, wide editorial photography"},
        {"slug": "how-much-does-amazon-fba-cost-per-item-a-complete-breakdown-1", "size": "img1",
         "prompt": "Close-up of a product package being labeled in a warehouse, shipping concept editorial"},
        {"slug": "how-much-does-amazon-fba-cost-per-item-a-complete-breakdown-2", "size": "img2",
         "prompt": "Warehouse worker scanning barcodes on shelves, fulfillment operations atmosphere editorial"},

        # amazon-fba-fee-calculator-2025-every-fee-explained-with-examples
        {"slug": "amazon-fba-fee-calculator-2025-every-fee-explained-with-examples-hero", "size": "hero",
         "prompt": "Boxes and packages on a conveyor belt in a logistics center, fee breakdown concept editorial"},
        {"slug": "amazon-fba-fee-calculator-2025-every-fee-explained-with-examples-1", "size": "img1",
         "prompt": "Product packaging box with a shipping label, cost per unit concept, clean editorial still life"},
        {"slug": "amazon-fba-fee-calculator-2025-every-fee-explained-with-examples-2", "size": "img2",
         "prompt": "Ecommerce seller packaging products at a home desk, FBA prep concept, editorial photography"},

        # ebay-fee-calculator-2025-final-value-insertion-and-store-costs
        {"slug": "ebay-fee-calculator-2025-final-value-insertion-and-store-costs-hero", "size": "hero",
         "prompt": "Online marketplace seller photographing products for listing, ecommerce concept editorial photography"},
        {"slug": "ebay-fee-calculator-2025-final-value-insertion-and-store-costs-1", "size": "img1",
         "prompt": "Products arranged for professional photography on a white background, seller product listing editorial"},
        {"slug": "ebay-fee-calculator-2025-final-value-insertion-and-store-costs-2", "size": "img2",
         "prompt": "Seller reviewing sold items and packing orders at home, marketplace selling atmosphere"},

        # etsy-fee-calculator-2025-transaction-payment-and-offsite-ad-costs
        {"slug": "etsy-fee-calculator-2025-transaction-payment-and-offsite-ad-costs-hero", "size": "hero",
         "prompt": "Handmade craft products arranged on a wooden table, artisan seller concept, warm editorial photography"},
        {"slug": "etsy-fee-calculator-2025-transaction-payment-and-offsite-ad-costs-1", "size": "img1",
         "prompt": "Artisan workshop with handmade goods, warm light, creative seller atmosphere editorial"},
        {"slug": "etsy-fee-calculator-2025-transaction-payment-and-offsite-ad-costs-2", "size": "img2",
         "prompt": "Handmade goods in tissue paper and boxes, small business packaging concept, warm editorial"},

        # dropshipping-profit-margin-calculator-find-your-true-net-profit
        {"slug": "dropshipping-profit-margin-calculator-find-your-true-net-profit-hero", "size": "hero",
         "prompt": "Package being shipped from supplier directly to customer, dropshipping logistics concept editorial"},
        {"slug": "dropshipping-profit-margin-calculator-find-your-true-net-profit-1", "size": "img1",
         "prompt": "Laptop showing an online store with products, blurred interface, dropshipping concept editorial"},
        {"slug": "dropshipping-profit-margin-calculator-find-your-true-net-profit-2", "size": "img2",
         "prompt": "Supply chain diagram represented by boxes and arrows on a table, dropshipping flow editorial"},

        # how-to-calculate-net-profit-in-ecommerce-a-sellers-guide
        {"slug": "how-to-calculate-net-profit-in-ecommerce-a-sellers-guide-hero", "size": "hero",
         "prompt": "Ecommerce seller reviewing financial results on a laptop, success concept, warm editorial photography"},
        {"slug": "how-to-calculate-net-profit-in-ecommerce-a-sellers-guide-1", "size": "img1",
         "prompt": "Coins arranged to show profit calculation concept, warm editorial still life"},
        {"slug": "how-to-calculate-net-profit-in-ecommerce-a-sellers-guide-2", "size": "img2",
         "prompt": "Online store revenue dashboard blurred on a screen, positive profit concept editorial"},
    ],

    # =========================================================================
    "tripcostcalc.com": [
        # japan-trip-budget-calculator-2025-plan-your-perfect-visit
        {"slug": "japan-trip-budget-calculator-2025-plan-your-perfect-visit-hero", "size": "hero",
         "prompt": "Mount Fuji reflected in a calm lake with cherry blossoms in foreground, iconic Japan travel editorial"},
        {"slug": "japan-trip-budget-calculator-2025-plan-your-perfect-visit-1", "size": "img1",
         "prompt": "Japanese street food stall at night with colorful lanterns, warm atmospheric travel editorial"},
        {"slug": "japan-trip-budget-calculator-2025-plan-your-perfect-visit-2", "size": "img2",
         "prompt": "Shinkansen bullet train passing under Mount Fuji at sunset, Japan travel editorial photography"},

        # how-much-does-a-trip-to-japan-cost-2025-budget-breakdown
        {"slug": "how-much-does-a-trip-to-japan-cost-2025-budget-breakdown-hero", "size": "hero",
         "prompt": "Traditional Japanese ryokan garden with stone lanterns and pond, travel experience concept editorial"},
        {"slug": "how-much-does-a-trip-to-japan-cost-2025-budget-breakdown-1", "size": "img1",
         "prompt": "Tokyo skyline at golden hour with temple in foreground, Japan travel photography editorial"},
        {"slug": "how-much-does-a-trip-to-japan-cost-2025-budget-breakdown-2", "size": "img2",
         "prompt": "Japanese temple entrance with torii gate and autumn foliage, cultural travel editorial"},

        # travel-budget-calculator-by-destination-estimate-any-trip
        {"slug": "travel-budget-calculator-by-destination-estimate-any-trip-hero", "size": "hero",
         "prompt": "Traveler with a backpack at an airport terminal watching planes, trip planning concept editorial"},
        {"slug": "travel-budget-calculator-by-destination-estimate-any-trip-1", "size": "img1",
         "prompt": "Open travel journal with a passport on a wooden table, trip planning editorial still life"},
        {"slug": "travel-budget-calculator-by-destination-estimate-any-trip-2", "size": "img2",
         "prompt": "World map with travel pins stuck in various destinations, trip planning concept editorial overhead"},

        # backpacking-budget-by-country-2025-daily-costs-ranked
        {"slug": "backpacking-budget-by-country-2025-daily-costs-ranked-hero", "size": "hero",
         "prompt": "Backpacker walking a mountain trail at dawn with a dramatic landscape, adventure travel editorial"},
        {"slug": "backpacking-budget-by-country-2025-daily-costs-ranked-1", "size": "img1",
         "prompt": "Backpack and hiking boots beside a hostel bunk bed, budget travel concept editorial"},
        {"slug": "backpacking-budget-by-country-2025-daily-costs-ranked-2", "size": "img2",
         "prompt": "Backpackers eating street food at a local market in Southeast Asia, budget travel atmosphere"},

        # europe-rail-pass-cost-calculator-is-eurail-worth-it
        {"slug": "europe-rail-pass-cost-calculator-is-eurail-worth-it-hero", "size": "hero",
         "prompt": "High-speed train at a European train station with arched glass ceiling, rail travel editorial photography"},
        {"slug": "europe-rail-pass-cost-calculator-is-eurail-worth-it-1", "size": "img1",
         "prompt": "Train window view of European countryside passing by, rail journey atmosphere editorial"},
        {"slug": "europe-rail-pass-cost-calculator-is-eurail-worth-it-2", "size": "img2",
         "prompt": "Traveler with a suitcase boarding a European InterCity train, rail pass concept editorial"},

        # road-trip-cost-calculator-gas-hotels-food-and-fun
        {"slug": "road-trip-cost-calculator-gas-hotels-food-and-fun-hero", "size": "hero",
         "prompt": "Classic American road trip — convertible on Route 66 with desert scenery, vintage travel editorial"},
        {"slug": "road-trip-cost-calculator-gas-hotels-food-and-fun-1", "size": "img1",
         "prompt": "Road map spread on a car hood with a compass, road trip planning concept editorial"},
        {"slug": "road-trip-cost-calculator-gas-hotels-food-and-fun-2", "size": "img2",
         "prompt": "Road trip car packed with luggage, family loading up, adventure departure editorial photography"},
    ],

    # =========================================================================
    "workoutplanner.io": [
        # 3-day-workout-split-for-beginners-full-body-strength-plan
        {"slug": "3-day-workout-split-for-beginners-full-body-strength-plan-hero", "size": "hero",
         "prompt": "Beginner in a gym doing a dumbbell exercise, bright clean gym environment, fitness editorial photography"},
        {"slug": "3-day-workout-split-for-beginners-full-body-strength-plan-1", "size": "img1",
         "prompt": "Rack of colorful dumbbells in a gym, organized fitness equipment, editorial product photography"},
        {"slug": "3-day-workout-split-for-beginners-full-body-strength-plan-2", "size": "img2",
         "prompt": "Person completing a full body workout, squat position, clean bright gym, fitness motivation editorial"},

        # workout-split-for-busy-professionals-minimal-time-maximum-results
        {"slug": "workout-split-for-busy-professionals-minimal-time-maximum-results-hero", "size": "hero",
         "prompt": "Professional in gym clothes doing a quick workout in a home gym, efficient training concept editorial"},
        {"slug": "workout-split-for-busy-professionals-minimal-time-maximum-results-1", "size": "img1",
         "prompt": "Wristwatch beside gym gloves on a bench, time efficiency workout concept editorial"},
        {"slug": "workout-split-for-busy-professionals-minimal-time-maximum-results-2", "size": "img2",
         "prompt": "Compact home gym with minimal equipment, efficient workout space editorial photography"},

        # bodyweight-workout-plan-no-equipment-build-muscle-at-home
        {"slug": "bodyweight-workout-plan-no-equipment-build-muscle-at-home-hero", "size": "hero",
         "prompt": "Person doing push-ups on a yoga mat in a bright living room, no equipment workout concept editorial"},
        {"slug": "bodyweight-workout-plan-no-equipment-build-muscle-at-home-1", "size": "img1",
         "prompt": "Person in plank position on a mat, bodyweight exercise, clean editorial fitness photography"},
        {"slug": "bodyweight-workout-plan-no-equipment-build-muscle-at-home-2", "size": "img2",
         "prompt": "Home workout space with a yoga mat and water bottle, minimal equipment fitness concept editorial"},

        # full-body-workout-3-times-a-week-the-science-and-the-routine
        {"slug": "full-body-workout-3-times-a-week-the-science-and-the-routine-hero", "size": "hero",
         "prompt": "Athlete performing a compound barbell exercise in a well-equipped gym, full body training editorial"},
        {"slug": "full-body-workout-3-times-a-week-the-science-and-the-routine-1", "size": "img1",
         "prompt": "Barbell loaded with weights on a rack, gym equipment detail, editorial fitness photography"},
        {"slug": "full-body-workout-3-times-a-week-the-science-and-the-routine-2", "size": "img2",
         "prompt": "Weekly workout calendar on a gym wall, training schedule concept, atmospheric editorial"},

        # how-to-progressive-overload-at-home-no-gym-required
        {"slug": "how-to-progressive-overload-at-home-no-gym-required-hero", "size": "hero",
         "prompt": "Progressive set of different resistance bands and weights arranged by size, overload concept editorial"},
        {"slug": "how-to-progressive-overload-at-home-no-gym-required-1", "size": "img1",
         "prompt": "Close-up of a person's hand gripping a resistance band, home exercise detail editorial"},
        {"slug": "how-to-progressive-overload-at-home-no-gym-required-2", "size": "img2",
         "prompt": "Home fitness progress — person adding more resistance to an exercise, overload concept photography"},

        # progressive-overload-calculator-track-weight-increases-over-time
        {"slug": "progressive-overload-calculator-track-weight-increases-over-time-hero", "size": "hero",
         "prompt": "Training journal with workout logs on a gym floor, progress tracking concept, editorial fitness photography"},
        {"slug": "progressive-overload-calculator-track-weight-increases-over-time-1", "size": "img1",
         "prompt": "Close-up of a gym logbook with weight entries, training progress concept editorial"},
        {"slug": "progressive-overload-calculator-track-weight-increases-over-time-2", "size": "img2",
         "prompt": "Athlete celebrating a personal record lift in the gym, progress achievement concept editorial"},
    ],

    # =========================================================================
    "colorpalette.io": [
        # color-contrast-checker
        {"slug": "color-contrast-checker-hero", "size": "hero",
         "prompt": "Abstract overlapping color blocks in high and low contrast arrangements, visual design concept, clean editorial art"},
        {"slug": "color-contrast-checker-1", "size": "img1",
         "prompt": "Close-up of color swatches in contrasting pairs, vibrant editorial design photography"},
        {"slug": "color-contrast-checker-2", "size": "img2",
         "prompt": "Designer at a color-calibrated monitor working on visual accessibility, editorial photography"},

        # what-is-color-theory
        {"slug": "what-is-color-theory-hero", "size": "hero",
         "prompt": "Color wheel rendered beautifully with vibrant pigments, color theory concept, editorial design art photography"},
        {"slug": "what-is-color-theory-1", "size": "img1",
         "prompt": "Paint mixing on a palette with complementary colors, color theory editorial still life"},
        {"slug": "what-is-color-theory-2", "size": "img2",
         "prompt": "Spectrum of colors from a prism on a white surface, light and color theory editorial photography"},

        # color-palette-for-website
        {"slug": "color-palette-for-website-hero", "size": "hero",
         "prompt": "Designer's desk with color swatches and a laptop showing a beautiful website, warm editorial photography"},
        {"slug": "color-palette-for-website-1", "size": "img1",
         "prompt": "Fan of color swatch cards on a design desk, web palette concept editorial"},
        {"slug": "color-palette-for-website-2", "size": "img2",
         "prompt": "UI designer arranging color chips for a web project, professional design studio atmosphere"},

        # complementary-colors
        {"slug": "complementary-colors-hero", "size": "hero",
         "prompt": "Sunset with orange sky and blue ocean — perfect complementary color concept, atmospheric landscape editorial"},
        {"slug": "complementary-colors-1", "size": "img1",
         "prompt": "Orange and blue abstract paint splashes, complementary colors concept, vibrant editorial art"},
        {"slug": "complementary-colors-2", "size": "img2",
         "prompt": "Purple flowers against a yellow field, natural complementary colors, beautiful landscape editorial"},

        # wcag-color-contrast-requirements
        {"slug": "wcag-color-contrast-requirements-hero", "size": "hero",
         "prompt": "Clean design studio with accessibility guidelines pinned to a board, professional editorial photography"},
        {"slug": "wcag-color-contrast-requirements-1", "size": "img1",
         "prompt": "High contrast graphic design sample in black and white, accessibility concept editorial art"},
        {"slug": "wcag-color-contrast-requirements-2", "size": "img2",
         "prompt": "Designer checking color accessibility on a calibrated monitor, professional workflow editorial"},

        # how-to-choose-brand-colors
        {"slug": "how-to-choose-brand-colors-hero", "size": "hero",
         "prompt": "Brand mood board with fabric swatches, paint chips, and product samples, brand identity editorial"},
        {"slug": "how-to-choose-brand-colors-1", "size": "img1",
         "prompt": "Color psychology samples arranged by emotional category, warm and cool tones, brand concept"},
        {"slug": "how-to-choose-brand-colors-2", "size": "img2",
         "prompt": "Marketing team discussing brand color options at a whiteboard, creative session editorial"},
    ],

    # =========================================================================
    "favicongen.io": [
        # apple-touch-icon
        {"slug": "apple-touch-icon-hero", "size": "hero",
         "prompt": "iPhone home screen with app icons arranged neatly, warm light, mobile design concept editorial photography"},
        {"slug": "apple-touch-icon-1", "size": "img1",
         "prompt": "Close-up of iOS app icons on a phone screen, rounded squares, warm editorial tech photography"},
        {"slug": "apple-touch-icon-2", "size": "img2",
         "prompt": "Apple device collection on a white desk, product photography editorial, clean minimalist concept"},

        # favicon-sizes
        {"slug": "favicon-sizes-hero", "size": "hero",
         "prompt": "Multiple browser tabs visible in different sizes with blurred tab icons, web browser editorial concept"},
        {"slug": "favicon-sizes-1", "size": "img1",
         "prompt": "Pixel grid magnified showing icon sizes, zoomed in design concept, editorial tech art"},
        {"slug": "favicon-sizes-2", "size": "img2",
         "prompt": "Design workspace with multiple screen sizes tested, responsive favicon concept editorial"},

        # favicon-ico-vs-png
        {"slug": "favicon-ico-vs-png-hero", "size": "hero",
         "prompt": "Two file types represented as elegant objects on a clean desk, format comparison concept editorial"},
        {"slug": "favicon-ico-vs-png-1", "size": "img1",
         "prompt": "Close-up of two different image file icons blurred on a screen, file format concept editorial"},
        {"slug": "favicon-ico-vs-png-2", "size": "img2",
         "prompt": "Web developer comparing icon formats on a monitor, professional editorial photography"},

        # how-to-create-a-favicon
        {"slug": "how-to-create-a-favicon-hero", "size": "hero",
         "prompt": "Designer at a pixel art editor creating a tiny icon, close-up editorial photography"},
        {"slug": "how-to-create-a-favicon-1", "size": "img1",
         "prompt": "Drawing tablet with a small icon being designed, blurred screen, design process editorial"},
        {"slug": "how-to-create-a-favicon-2", "size": "img2",
         "prompt": "Web design studio setup with a monitor showing icon creation, warm editorial photography"},

        # favicon-not-showing
        {"slug": "favicon-not-showing-hero", "size": "hero",
         "prompt": "Browser window with a blank gray tab icon visible, debugging concept, editorial tech photography"},
        {"slug": "favicon-not-showing-1", "size": "img1",
         "prompt": "Developer looking at a browser tab with a missing icon, troubleshooting atmosphere editorial"},
        {"slug": "favicon-not-showing-2", "size": "img2",
         "prompt": "Web inspector DevTools open on a browser, debugging concept, warm developer editorial"},

        # what-is-a-favicon
        {"slug": "what-is-a-favicon-hero", "size": "hero",
         "prompt": "Browser with multiple colorful tabs visible, favicon icons on each tab, web browsing concept editorial"},
        {"slug": "what-is-a-favicon-1", "size": "img1",
         "prompt": "Magnifying glass over a browser tab showing a tiny icon, favicon close-up concept"},
        {"slug": "what-is-a-favicon-2", "size": "img2",
         "prompt": "Laptop in a coffee shop with browser tabs open, everyday web browsing atmosphere editorial"},
    ],

    # =========================================================================
    "flexplay.io": [
        # css-flexbox-tutorial
        {"slug": "css-flexbox-tutorial-hero", "size": "hero",
         "prompt": "Abstract geometric boxes arranged in flex patterns, colorful layout visualization, modern graphic design editorial"},
        {"slug": "css-flexbox-tutorial-1", "size": "img1",
         "prompt": "Developer at a dual monitor setup coding, blurred code on screen, warm editorial photography"},
        {"slug": "css-flexbox-tutorial-2", "size": "img2",
         "prompt": "Colorful rectangular blocks arranged in rows and columns on a white surface, layout concept editorial"},

        # holy-grail-layout-css
        {"slug": "holy-grail-layout-css-hero", "size": "hero",
         "prompt": "Beautiful web page layout visualized as architectural blueprint with sections, design concept editorial art"},
        {"slug": "holy-grail-layout-css-1", "size": "img1",
         "prompt": "Architectural grid overlay on a modern webpage mockup, layout structure concept editorial"},
        {"slug": "holy-grail-layout-css-2", "size": "img2",
         "prompt": "Web designer sketching a page layout on a large paper, design planning atmosphere editorial"},

        # what-is-flexbox
        {"slug": "what-is-flexbox-hero", "size": "hero",
         "prompt": "Colorful flexible rubber bands arranged in patterns, flexbox concept metaphor, editorial product art"},
        {"slug": "what-is-flexbox-1", "size": "img1",
         "prompt": "Stretching and aligning colored blocks in a grid, flexbox alignment concept, editorial graphic art"},
        {"slug": "what-is-flexbox-2", "size": "img2",
         "prompt": "Web developer explaining layout on a whiteboard with boxes and arrows, tutorial atmosphere"},

        # flexbox-cheat-sheet
        {"slug": "flexbox-cheat-sheet-hero", "size": "hero",
         "prompt": "Reference cards and technical cards arranged on a developer desk, warm editorial photography, no readable text"},
        {"slug": "flexbox-cheat-sheet-1", "size": "img1",
         "prompt": "Reference document being printed, close-up of code patterns, warm editorial detail"},
        {"slug": "flexbox-cheat-sheet-2", "size": "img2",
         "prompt": "Developer desk with pinned cheat sheets and multiple monitors, warm workspace editorial"},

        # flexbox-vs-grid
        {"slug": "flexbox-vs-grid-hero", "size": "hero",
         "prompt": "Abstract one-dimensional line pattern next to a two-dimensional grid pattern, layout comparison art editorial"},
        {"slug": "flexbox-vs-grid-1", "size": "img1",
         "prompt": "Single row of boxes versus a 2D grid of boxes arranged side by side, concept art editorial"},
        {"slug": "flexbox-vs-grid-2", "size": "img2",
         "prompt": "Two different layout blueprints on a designer's table, comparison concept editorial photography"},

        # flexbox-interview-questions
        {"slug": "flexbox-interview-questions-hero", "size": "hero",
         "prompt": "Professional tech interview setup — laptop, notepad, clean desk, warm editorial photography, interview concept"},
        {"slug": "flexbox-interview-questions-1", "size": "img1",
         "prompt": "Close-up of a laptop showing code, interview prep concept, blurred screen editorial"},
        {"slug": "flexbox-interview-questions-2", "size": "img2",
         "prompt": "Software developer interview in a modern office, professional atmosphere editorial photography"},
    ],

    # =========================================================================
    "freepbrtextures.com": [
        # pbr-textures-in-unity
        {"slug": "pbr-textures-in-unity-hero", "size": "hero",
         "prompt": "3D rendered scene inside a game engine with realistic PBR materials on surfaces, atmospheric visualization"},
        {"slug": "pbr-textures-in-unity-1", "size": "img1",
         "prompt": "Game engine viewport showing a 3D object with PBR material applied, blurred software UI, editorial tech"},
        {"slug": "pbr-textures-in-unity-2", "size": "img2",
         "prompt": "3D artist at a workstation with a realistic game scene on screen, warm developer editorial photography"},

        # how-to-make-tileable-texture
        {"slug": "how-to-make-tileable-texture-hero", "size": "hero",
         "prompt": "Seamless brick texture tiles repeating perfectly into a large wall, tileable pattern concept editorial"},
        {"slug": "how-to-make-tileable-texture-1", "size": "img1",
         "prompt": "Texture closeup showing perfectly matching seam where tile repeats, seamless quality editorial"},
        {"slug": "how-to-make-tileable-texture-2", "size": "img2",
         "prompt": "Artist painting a texture in a photo editor, zoom in/out workflow, warm editorial photography"},

        # pbr-workflow-explained
        {"slug": "pbr-workflow-explained-hero", "size": "hero",
         "prompt": "PBR texture map channels laid out — albedo, roughness, normal — as abstract colored layers, 3D art concept"},
        {"slug": "pbr-workflow-explained-1", "size": "img1",
         "prompt": "3D sphere showing PBR material preview with realistic lighting, metallic surface editorial render"},
        {"slug": "pbr-workflow-explained-2", "size": "img2",
         "prompt": "Material authoring workflow in a 3D software, nodes and connections blurred, atmosphere editorial"},

        # what-is-a-seamless-texture
        {"slug": "what-is-a-seamless-texture-hero", "size": "hero",
         "prompt": "Repeating wood grain texture perfectly tiled, seamless pattern concept, beautiful material editorial photography"},
        {"slug": "what-is-a-seamless-texture-1", "size": "img1",
         "prompt": "Close-up of a perfectly repeating stone texture, high-detail seamless surface editorial"},
        {"slug": "what-is-a-seamless-texture-2", "size": "img2",
         "prompt": "Tiled floor in a building with a perfectly seamless pattern, architecture texture concept editorial"},

        # what-is-pbr-texture
        {"slug": "what-is-pbr-texture-hero", "size": "hero",
         "prompt": "Realistic PBR sphere with metallic and rough materials side by side, 3D rendering concept editorial"},
        {"slug": "what-is-pbr-texture-1", "size": "img1",
         "prompt": "Material sphere showcase with different PBR properties — glossy, matte, metallic — editorial render"},
        {"slug": "what-is-pbr-texture-2", "size": "img2",
         "prompt": "3D artist admiring a photorealistic rendered scene in a dark studio, PBR achievement concept"},

        # ai-texture-generators
        {"slug": "ai-texture-generators-hero", "size": "hero",
         "prompt": "Computer generating a photorealistic texture in real-time, AI creation concept, atmospheric digital art editorial"},
        {"slug": "ai-texture-generators-1", "size": "img1",
         "prompt": "GPU server room with green status lights, AI computing infrastructure, atmospheric tech editorial"},
        {"slug": "ai-texture-generators-2", "size": "img2",
         "prompt": "Digital artist comparing AI-generated and traditional textures on dual monitors, editorial photography"},

        # welcome
        {"slug": "welcome-hero", "size": "hero",
         "prompt": "Beautiful material library showcase with various textures arranged elegantly, warm editorial photography"},
        {"slug": "welcome-1", "size": "img1",
         "prompt": "Wood, stone, and metal material samples arranged artistically, PBR texture collection editorial"},
        {"slug": "welcome-2", "size": "img2",
         "prompt": "3D artist's workspace with texture samples and a rendering setup, welcome concept editorial"},

        # pbr-textures-in-blender
        {"slug": "pbr-textures-in-blender-hero", "size": "hero",
         "prompt": "Blender 3D viewport showing a photorealistic render with PBR materials, blurred UI editorial photography"},
        {"slug": "pbr-textures-in-blender-1", "size": "img1",
         "prompt": "Node editor with material nodes connected, blurred screenshot, Blender workflow concept editorial"},
        {"slug": "pbr-textures-in-blender-2", "size": "img2",
         "prompt": "3D artist at a Blender workstation rendering a realistic scene, warm editorial photography"},

        # normal-map-vs-height-map
        {"slug": "normal-map-vs-height-map-hero", "size": "hero",
         "prompt": "Surface with normal mapping creating depth illusion versus flat surface, dramatic 3D lighting editorial"},
        {"slug": "normal-map-vs-height-map-1", "size": "img1",
         "prompt": "Close-up of a blue-purple normal map texture, iconic PBR detail editorial"},
        {"slug": "normal-map-vs-height-map-2", "size": "img2",
         "prompt": "Two identical objects with different depth map techniques side by side, comparison render editorial"},

        # roughness-vs-glossiness
        {"slug": "roughness-vs-glossiness-hero", "size": "hero",
         "prompt": "Two material spheres — one matte and one glossy — on a studio backdrop, PBR properties editorial render"},
        {"slug": "roughness-vs-glossiness-1", "size": "img1",
         "prompt": "Rough stone surface next to a polished marble surface, texture contrast editorial photography"},
        {"slug": "roughness-vs-glossiness-2", "size": "img2",
         "prompt": "Material gradient from completely matte to perfectly reflective, roughness spectrum render editorial"},

        # pbr-textures-in-unreal
        {"slug": "pbr-textures-in-unreal-hero", "size": "hero",
         "prompt": "Unreal Engine scene with photorealistic environment and materials, atmospheric game engine visualization"},
        {"slug": "pbr-textures-in-unreal-1", "size": "img1",
         "prompt": "Game engine material editor with nodes blurred, Unreal workflow concept, editorial tech photography"},
        {"slug": "pbr-textures-in-unreal-2", "size": "img2",
         "prompt": "Game developer reviewing Unreal Engine scene quality on a large monitor, editorial photography"},
    ],

    # =========================================================================
    "howmanycoin.com": [
        # crypto-exchange-rates-explained
        {"slug": "crypto-exchange-rates-explained-hero", "size": "hero",
         "prompt": "Abstract cryptocurrency market visualization — rising lines and glowing nodes, atmospheric digital finance editorial"},
        {"slug": "crypto-exchange-rates-explained-1", "size": "img1",
         "prompt": "Bitcoin and Ethereum coins on a dark surface with dramatic lighting, crypto editorial photography"},
        {"slug": "crypto-exchange-rates-explained-2", "size": "img2",
         "prompt": "Exchange rate board in a financial district, blurred numbers, crypto market concept editorial"},

        # how-to-calculate-crypto-market-cap
        {"slug": "how-to-calculate-crypto-market-cap-hero", "size": "hero",
         "prompt": "Cryptocurrency market visualization — glowing coins in a dark space, market cap concept editorial art"},
        {"slug": "how-to-calculate-crypto-market-cap-1", "size": "img1",
         "prompt": "Physical gold and cryptocurrency coins stacked together, market value concept editorial"},
        {"slug": "how-to-calculate-crypto-market-cap-2", "size": "img2",
         "prompt": "Financial analyst viewing crypto market data on screens, professional editorial photography"},

        # welcome
        {"slug": "welcome-hero", "size": "hero",
         "prompt": "Cryptocurrency ecosystem visualization — interconnected coins and blockchain nodes, atmospheric digital art"},
        {"slug": "welcome-1", "size": "img1",
         "prompt": "Various cryptocurrency coin symbols arranged artistically, dark background, editorial product photography"},
        {"slug": "welcome-2", "size": "img2",
         "prompt": "Person exploring cryptocurrency portfolio on a laptop in a modern office, welcome editorial"},

        # what-is-circulating-supply
        {"slug": "what-is-circulating-supply-hero", "size": "hero",
         "prompt": "Coins flowing in a circular motion, circulation concept, abstract cryptocurrency editorial art"},
        {"slug": "what-is-circulating-supply-1", "size": "img1",
         "prompt": "Bitcoin coins arranged in a circle symbolizing circulation, dark editorial photography"},
        {"slug": "what-is-circulating-supply-2", "size": "img2",
         "prompt": "Supply and demand visualization as flowing liquids, abstract financial concept editorial"},

        # how-many-cryptocurrencies-exist
        {"slug": "how-many-cryptocurrencies-exist-hero", "size": "hero",
         "prompt": "Hundreds of glowing cryptocurrency tokens floating in space, ecosystem diversity concept editorial"},
        {"slug": "how-many-cryptocurrencies-exist-1", "size": "img1",
         "prompt": "Grid of various cryptocurrency logos blurred as lights, digital ecosystem editorial art"},
        {"slug": "how-many-cryptocurrencies-exist-2", "size": "img2",
         "prompt": "Digital asset landscape with countless tokens visualized as a galaxy, crypto universe editorial"},

        # how-to-convert-bitcoin-to-usd
        {"slug": "how-to-convert-bitcoin-to-usd-hero", "size": "hero",
         "prompt": "Bitcoin coin next to US dollar bills on a dark surface, conversion concept editorial photography"},
        {"slug": "how-to-convert-bitcoin-to-usd-1", "size": "img1",
         "prompt": "Close-up of a Bitcoin coin with dollar sign reflection, conversion concept editorial"},
        {"slug": "how-to-convert-bitcoin-to-usd-2", "size": "img2",
         "prompt": "Currency exchange booth with digital displays, Bitcoin to dollar concept editorial"},

        # what-is-crypto-market-cap
        {"slug": "what-is-crypto-market-cap-hero", "size": "hero",
         "prompt": "Crypto market overview visualization — large and small bubbles representing different coins, editorial art"},
        {"slug": "what-is-crypto-market-cap-1", "size": "img1",
         "prompt": "Market cap bubble chart with different sized spheres, financial visualization concept editorial"},
        {"slug": "what-is-crypto-market-cap-2", "size": "img2",
         "prompt": "Investor analyzing crypto market data on a trading screen, professional finance editorial"},
    ],

    # =========================================================================
    "makepicsmall.com": [
        # reduce-image-file-size-for-web
        {"slug": "reduce-image-file-size-for-web-hero", "size": "hero",
         "prompt": "Stack of photos reducing in size conceptually, compression theme, warm editorial photography still life"},
        {"slug": "reduce-image-file-size-for-web-1", "size": "img1",
         "prompt": "Close-up of a camera lens with web optimization concept, clean product editorial photography"},
        {"slug": "reduce-image-file-size-for-web-2", "size": "img2",
         "prompt": "Web designer optimizing images on a laptop, performance improvement concept, editorial photography"},

        # welcome
        {"slug": "welcome-hero", "size": "hero",
         "prompt": "Beautiful photography workstation with professional camera and laptop, image editing concept editorial"},
        {"slug": "welcome-1", "size": "img1",
         "prompt": "Camera, photos, and editing tools on a wooden desk, photography concept editorial still life"},
        {"slug": "welcome-2", "size": "img2",
         "prompt": "Photographer reviewing images on a bright iMac, image management atmosphere editorial"},

        # compress-jpg-to-100kb
        {"slug": "compress-jpg-to-100kb-hero", "size": "hero",
         "prompt": "Photo printing process with size reduction concept, photography workflow editorial photography"},
        {"slug": "compress-jpg-to-100kb-1", "size": "img1",
         "prompt": "Small printed photo next to a large digital screen, size contrast concept editorial"},
        {"slug": "compress-jpg-to-100kb-2", "size": "img2",
         "prompt": "Website loading with optimized images visible, performance concept editorial photography"},

        # shrink-photo-for-whatsapp
        {"slug": "shrink-photo-for-whatsapp-hero", "size": "hero",
         "prompt": "Smartphone screen with a messaging app, photo sharing concept, warm editorial mobile photography"},
        {"slug": "shrink-photo-for-whatsapp-1", "size": "img1",
         "prompt": "Phone in hand with messaging app open, photo attachment concept, warm editorial photography"},
        {"slug": "shrink-photo-for-whatsapp-2", "size": "img2",
         "prompt": "People sharing photos on phones at a social gathering, mobile photo concept editorial"},

        # jpg-vs-png-vs-webp
        {"slug": "jpg-vs-png-vs-webp-hero", "size": "hero",
         "prompt": "Three elegant file format representations as abstract colored cards on a desk, comparison concept editorial"},
        {"slug": "jpg-vs-png-vs-webp-1", "size": "img1",
         "prompt": "Image quality comparison concept — two photos side by side, one crisp one compressed, editorial"},
        {"slug": "jpg-vs-png-vs-webp-2", "size": "img2",
         "prompt": "Web developer testing different image formats in a browser, format comparison atmosphere editorial"},

        # compress-png-to-100kb
        {"slug": "compress-png-to-100kb-hero", "size": "hero",
         "prompt": "Transparent graphic design assets arranged on a laptop, PNG compression concept editorial"},
        {"slug": "compress-png-to-100kb-1", "size": "img1",
         "prompt": "Design files and export settings on a screen, blurred UI, compression workflow editorial"},
        {"slug": "compress-png-to-100kb-2", "size": "img2",
         "prompt": "Graphic designer exporting web assets, professional workflow editorial photography"},

        # compress-jpg-to-500kb
        {"slug": "compress-jpg-to-500kb-hero", "size": "hero",
         "prompt": "Beautiful landscape photograph being prepared for web, editorial photography optimization concept"},
        {"slug": "compress-jpg-to-500kb-1", "size": "img1",
         "prompt": "Photo editor interface blurred showing compression settings, image optimization editorial"},
        {"slug": "compress-jpg-to-500kb-2", "size": "img2",
         "prompt": "Photographer transferring photos from camera to laptop, image workflow editorial photography"},
    ],

    # =========================================================================
    "pomotimer.io": [
        # what-is-the-pomodoro-technique
        {"slug": "what-is-the-pomodoro-technique-hero", "size": "hero",
         "prompt": "Red tomato-shaped kitchen timer on a clean desk with notebook and coffee, Pomodoro concept editorial photography"},
        {"slug": "what-is-the-pomodoro-technique-1", "size": "img1",
         "prompt": "Close-up of a red timer set to 25 minutes, focus concept editorial detail photography"},
        {"slug": "what-is-the-pomodoro-technique-2", "size": "img2",
         "prompt": "Productive workspace with a timer, coffee, and open notebook, Pomodoro atmosphere editorial"},

        # how-to-use-pomodoro-technique
        {"slug": "how-to-use-pomodoro-technique-hero", "size": "hero",
         "prompt": "Person deeply focused at a desk with a timer visible, concentration concept editorial photography"},
        {"slug": "how-to-use-pomodoro-technique-1", "size": "img1",
         "prompt": "Timer ticking beside a checklist of tasks, work session concept editorial still life"},
        {"slug": "how-to-use-pomodoro-technique-2", "size": "img2",
         "prompt": "Short break outside with a cup of coffee, Pomodoro rest interval concept editorial"},

        # pomodoro-technique-benefits
        {"slug": "pomodoro-technique-benefits-hero", "size": "hero",
         "prompt": "Person feeling accomplished after a productive work session, relaxed and satisfied, benefits concept editorial"},
        {"slug": "pomodoro-technique-benefits-1", "size": "img1",
         "prompt": "Completed task list on paper, productivity achievement concept, warm editorial still life"},
        {"slug": "pomodoro-technique-benefits-2", "size": "img2",
         "prompt": "Energized worker at a bright desk, work benefits and focus concept editorial photography"},

        # 52-17-rule
        {"slug": "52-17-rule-hero", "size": "hero",
         "prompt": "Clock showing 52 minutes in a productive workspace, focus and break rhythm concept editorial"},
        {"slug": "52-17-rule-1", "size": "img1",
         "prompt": "Desk clock closeup showing work interval time, productivity rhythm concept editorial"},
        {"slug": "52-17-rule-2", "size": "img2",
         "prompt": "Person taking a 17-minute walking break outside, work-rest balance concept editorial photography"},

        # pomodoro-timer-25-minutes
        {"slug": "pomodoro-timer-25-minutes-hero", "size": "hero",
         "prompt": "Digital timer glowing on a desk in a focused work environment, 25-minute session concept editorial"},
        {"slug": "pomodoro-timer-25-minutes-1", "size": "img1",
         "prompt": "Smartphone timer app counting down, blurred interface, focus session concept editorial"},
        {"slug": "pomodoro-timer-25-minutes-2", "size": "img2",
         "prompt": "Focused work environment at dusk, timer glow and laptop light, productivity atmosphere editorial"},

        # focus-techniques-for-studying
        {"slug": "focus-techniques-for-studying-hero", "size": "hero",
         "prompt": "Student in deep concentration at a clean study desk with soft lamp light, focus editorial photography"},
        {"slug": "focus-techniques-for-studying-1", "size": "img1",
         "prompt": "Close-up of noise-canceling headphones on a desk, focus tool concept, editorial product photography"},
        {"slug": "focus-techniques-for-studying-2", "size": "img2",
         "prompt": "Quiet library corner with a student studying, focus atmosphere editorial photography"},
    ],

    # =========================================================================
    "quickcurrency.io": [
        # travel-money-tips
        {"slug": "travel-money-tips-hero", "size": "hero",
         "prompt": "Various foreign currency notes spread on a map, international travel money concept editorial photography"},
        {"slug": "travel-money-tips-1", "size": "img1",
         "prompt": "Close-up of different foreign coins, world currency concept editorial photography"},
        {"slug": "travel-money-tips-2", "size": "img2",
         "prompt": "Traveler at a currency exchange booth with foreign bills in hand, editorial travel photography"},

        # usd-to-eur-exchange-rate
        {"slug": "usd-to-eur-exchange-rate-hero", "size": "hero",
         "prompt": "US dollar and Euro bills side by side, currency exchange concept, clean editorial financial photography"},
        {"slug": "usd-to-eur-exchange-rate-1", "size": "img1",
         "prompt": "Close-up of US dollar bills and Euro coins arranged together, exchange rate editorial"},
        {"slug": "usd-to-eur-exchange-rate-2", "size": "img2",
         "prompt": "European and American city landmarks juxtaposed, USD-EUR exchange concept editorial"},

        # how-currency-exchange-rates-work
        {"slug": "how-currency-exchange-rates-work-hero", "size": "hero",
         "prompt": "Currency trading floor with people and screens, exchange rate concept, professional editorial photography"},
        {"slug": "how-currency-exchange-rates-work-1", "size": "img1",
         "prompt": "Close-up of currency exchange rate board at an airport, blurred numbers, concept editorial"},
        {"slug": "how-currency-exchange-rates-work-2", "size": "img2",
         "prompt": "Forex trading concept — multiple currency symbols floating, abstract financial visualization"},

        # best-time-to-exchange-currency
        {"slug": "best-time-to-exchange-currency-hero", "size": "hero",
         "prompt": "Clock overlaid with foreign currency notes, optimal timing concept, editorial financial art"},
        {"slug": "best-time-to-exchange-currency-1", "size": "img1",
         "prompt": "Watch beside currency bills on a trading desk, timing concept editorial still life"},
        {"slug": "best-time-to-exchange-currency-2", "size": "img2",
         "prompt": "Currency exchange rate chart showing the best moment to convert, atmospheric financial visualization"},

        # what-affects-currency-exchange-rates
        {"slug": "what-affects-currency-exchange-rates-hero", "size": "hero",
         "prompt": "Global financial concept — currency notes, coins from multiple countries, world economy editorial"},
        {"slug": "what-affects-currency-exchange-rates-1", "size": "img1",
         "prompt": "Central bank building exterior, monetary policy concept, architectural editorial photography"},
        {"slug": "what-affects-currency-exchange-rates-2", "size": "img2",
         "prompt": "Financial market data on screens showing global currency movements, atmospheric editorial"},

        # bank-exchange-rate-vs-market-rate
        {"slug": "bank-exchange-rate-vs-market-rate-hero", "size": "hero",
         "prompt": "Bank branch next to a currency exchange kiosk, institutional vs market comparison concept editorial"},
        {"slug": "bank-exchange-rate-vs-market-rate-1", "size": "img1",
         "prompt": "Bank window with a teller, currency exchange service concept, editorial banking photography"},
        {"slug": "bank-exchange-rate-vs-market-rate-2", "size": "img2",
         "prompt": "Two exchange rate displays side by side, blurred numbers, comparison concept editorial"},
    ],

    # =========================================================================
    "worldclock.io": [
        # daylight-saving-time-explained
        {"slug": "daylight-saving-time-explained-hero", "size": "hero",
         "prompt": "Clock hands being moved forward in spring sunlight, daylight saving time concept, warm editorial photography"},
        {"slug": "daylight-saving-time-explained-1", "size": "img1",
         "prompt": "Close-up of a clock with hands at spring forward time, daylight saving concept editorial"},
        {"slug": "daylight-saving-time-explained-2", "size": "img2",
         "prompt": "Golden sunrise through bedroom curtains, extra daylight concept, atmospheric morning editorial"},

        # us-time-zones
        {"slug": "us-time-zones-hero", "size": "hero",
         "prompt": "Four clocks showing different US time zones displayed in a row, clean editorial product photography"},
        {"slug": "us-time-zones-1", "size": "img1",
         "prompt": "Wall of clocks showing different times, time zone concept, editorial photography"},
        {"slug": "us-time-zones-2", "size": "img2",
         "prompt": "American continent map with light and shadow showing day-night across time zones, atmospheric concept"},

        # est-vs-edt
        {"slug": "est-vs-edt-hero", "size": "hero",
         "prompt": "Two clocks side by side showing one hour difference, EDT vs EST concept editorial photography"},
        {"slug": "est-vs-edt-1", "size": "img1",
         "prompt": "Clock showing the transition between standard and daylight time, seasonal concept editorial"},
        {"slug": "est-vs-edt-2", "size": "img2",
         "prompt": "New York City skyline at winter dusk vs summer evening, seasonal time difference editorial"},

        # how-to-schedule-meetings-across-time-zones
        {"slug": "how-to-schedule-meetings-across-time-zones-hero", "size": "hero",
         "prompt": "Global team video call setup with multiple time zone clocks visible, remote collaboration editorial"},
        {"slug": "how-to-schedule-meetings-across-time-zones-1", "size": "img1",
         "prompt": "World map with multiple time overlay, international meeting scheduling concept editorial"},
        {"slug": "how-to-schedule-meetings-across-time-zones-2", "size": "img2",
         "prompt": "Professional at a laptop scheduling a global meeting, time zone management atmosphere editorial"},

        # what-is-utc
        {"slug": "what-is-utc-hero", "size": "hero",
         "prompt": "Atomic clock facility with precision timekeeping equipment, UTC reference concept, editorial photography"},
        {"slug": "what-is-utc-1", "size": "img1",
         "prompt": "Close-up of a precision atomic clock instrument, timekeeping concept editorial photography"},
        {"slug": "what-is-utc-2", "size": "img2",
         "prompt": "Greenwich Observatory building with a meridian line, UTC origin concept, atmospheric editorial"},

        # world-clock-online
        {"slug": "world-clock-online-hero", "size": "hero",
         "prompt": "World map at night with city lights glowing across all time zones, global time concept editorial"},
        {"slug": "world-clock-online-1", "size": "img1",
         "prompt": "Laptop showing a world time dashboard with multiple city clocks, blurred interface editorial"},
        {"slug": "world-clock-online-2", "size": "img2",
         "prompt": "Traveler checking a world clock app on a phone at an international airport, editorial photography"},
    ],
}

SITE_ORDER = [
    "carleasecalc.com", "freeinvoicemake.com", "gradecalc.io", "isitdown.fyi",
    "myfreelancerate.com", "paintcalc.io", "pickthestack.com", "recipescale.io",
    "rentalyieldcalc.com", "rentwatch.io", "sellerprofit.io", "tripcostcalc.com",
    "workoutplanner.io", "colorpalette.io", "favicongen.io", "flexplay.io",
    "freepbrtextures.com", "howmanycoin.com", "makepicsmall.com", "pomotimer.io",
    "quickcurrency.io", "worldclock.io",
]


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


def generate_image(spec: dict, output_dir: str, skip_existing: bool = True) -> str:
    slug = spec["slug"]
    size_key = spec["size"]
    prompt = spec["prompt"]
    target_w, target_h = SIZES[size_key]

    out_path = os.path.join(output_dir, f"{slug}.png")
    if skip_existing and os.path.exists(out_path):
        print(f"  [skip] {slug}.png already exists", file=sys.stderr)
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


def run_site(site: str, resume: bool = True, test: bool = False):
    if site not in SITE_MANIFESTS:
        print(f"Unknown site: {site}. Available: {', '.join(SITE_ORDER)}", file=sys.stderr)
        sys.exit(1)

    specs = SITE_MANIFESTS[site]
    blog_output_dir = os.path.abspath(f"sites/{site}/public/images/blog")
    os.makedirs(blog_output_dir, exist_ok=True)

    if test:
        specs = specs[:1]  # first image only for test

    total = len(specs)
    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Site: {site} ({total} images)", file=sys.stderr)
    print(f"Output: {blog_output_dir}", file=sys.stderr)
    print(f"{'='*60}", file=sys.stderr)

    for i, spec in enumerate(specs, 1):
        print(f"[{i}/{total}]", file=sys.stderr)
        generate_image(spec, blog_output_dir, skip_existing=resume)

    done = len([s for s in specs if os.path.exists(os.path.join(blog_output_dir, f"{s['slug']}.png"))])
    print(f"  Site {site}: {done}/{total} images present", file=sys.stderr)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Generate INF-43 blog images for 22 sites (417 images total)"
    )
    parser.add_argument("--site", choices=SITE_ORDER, help="Run for a specific site only")
    parser.add_argument("--all-sites", action="store_true", help="Run all 22 sites in sequence")
    parser.add_argument("--test", action="store_true", help="Test: generate first image of the site only")
    parser.add_argument("--resume", action="store_true", default=True,
                        help="Skip already-existing images (default: True)")
    parser.add_argument("--force", action="store_true", help="Regenerate even if image exists")

    args = parser.parse_args()
    resume = not args.force

    if args.all_sites:
        for site in SITE_ORDER:
            run_site(site, resume=resume, test=False)
        total_sites = len(SITE_ORDER)
        total_images = sum(len(SITE_MANIFESTS[s]) for s in SITE_ORDER)
        print(f"\nDone! {total_sites} sites, {total_images} images.", file=sys.stderr)
        return

    if args.site:
        run_site(args.site, resume=resume, test=args.test)
        return

    parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
