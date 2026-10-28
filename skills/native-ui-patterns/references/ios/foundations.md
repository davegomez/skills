# iOS foundations

## Guidance

**Kit:** system colors come in Light and Dark pairs, with background, grouped background, label, fill, and separator tiers; Dark backgrounds split into base and elevated. Text styles run from Large Title to Caption 2 in regular and emphasized weights, and each scales across 7 standard and 5 accessibility Dynamic Type sizes. Liquid Glass ranges from clear and tinted small pills to frosted panels with an edge highlight and shadow; vibrant labels and fills on a material fade across 4 and 3 tiers. The soft scroll edge fades content toward the edge with no line. **Inferred adaptation:** use semantic color and text-style roles rather than fixed values, and check Dark appearance and the largest accessibility size. Exact values, rendering, motion, and contrast ratios remain **Unconfirmed**; verify them in current Apple documentation.

## Visual references

Choose the exact foundation question and open only its named image.

| Visual question / state | Matching capture(s) | What to inspect |
| --- | --- | --- |
| System colors and semantic tiers | Kit [colors](../../assets/ios/kit/colors.png) | Hues and grays split Light over Dark; background, grouped, label, fill, and separator tiers |
| Text styles, weights, and label tiers | Kit [text styles](../../assets/ios/kit/text-styles.png) | Style order, regular versus emphasized, italic variants, four label colors |
| Standard Dynamic Type sizes | Kit [Dynamic Type](../../assets/ios/kit/dynamic-type.png) | xSmall to xxxLarge columns, Large (Default), relative growth per style |
| Accessibility Dynamic Type sizes | Kit [accessibility sizes](../../assets/ios/kit/dynamic-type-accessibility.png) | AX1 to AX5 growth, Headline weight, widening line gaps |
| Liquid Glass sizes over light and dark ground | Kit [Liquid Glass](../../assets/ios/kit/liquid-glass.png) | Clear and tinted small pills, frosted medium and large panels, edge highlight, shadow |
| Vibrant labels and fills on a material | Kit [vibrancy](../../assets/ios/kit/material-vibrancy.png) | Label and fill tier fade over a photo, separator |
| Soft scroll edge effect | Kit [scroll edge](../../assets/ios/kit/scroll-edge-effect.png) | Gradient from both edges toward the middle, no hard line |

## Review checks

Check Light and Dark, default and accessibility text sizes, label legibility over materials, and content under the scroll edge.
