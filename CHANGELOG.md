## Individual App changelogs
[Miru](miru/changelog.md)\
[Asobu](asobu/changelog.md)\
[Talent](talent/changelog.md)\

## Alpha v3.0 - 6/10/2026
- **General**
    - Replaced graphene django with strawberry as main GraphQL module
    - Improve quality of repo and service layers
    - Improve interaction between apps via service layers
    - Standardize CDN links for image resourcing
    - Add Sivr as current CDN service

## Alpha v2.2 - 5/14/2026
- **General**
    - Change admin to use email field instead of username
    - Add background CDNs for media

- **Apps Updated**
    - Asobu

## Alpha v2.1 - 4/15/2026
- **General**
    - Update test db contents
    - Removed unused files

## Alpha v2.0 - 4/10/2026
- **General**
    - Convert token based auth to bearer authentication
    - Add middleware to utilize jwt tokens for GraphQL authentication

- **Apps Updated**
    - Miru
    - Users

## Alpha v1.1 - 3/20/2026
- **Apps Updated**
    - Asobu

## Alpha v1.0 - 3/19/2026
Dev note: After finalizing the base of miru and implementing a better way to input data through the help of Anilist API. The progress from this patch has been deemed big enough to jump from 0.6 to 1.0. Thank you to everyone involved through testing and suggestions - A.P

- **Apps Updated**
    - Miru
    - Talent

## Alpha v0.6 - 3/17/2026
- **General**
    - Add github actions for the following
        - Run unit tests on pr to main
        - Run python linter on pr to main
    - Improved code following pylinter suggestions

## Alpha v0.5 - 3/16/2026
- **Apps Updated**
    - Asobu *NEW*
    - Talent

## Alpha v0.4 - 3/9/2026
- **General**
    - Add base oauth journey via D2X Accounts

## Alpha v0.3 - 3/4/2026
- **Apps Updated**
    - Miru

## Alpha v0.2 - 2/8/2026
- **Apps Updated**
    - Talent *NEW*

## Alpha v0.1 - 2/24/2026 INITIAL
Dev note: Codebase up to this points comes from previous iterations of Arcadia concept testing
- **Apps Updated**
    - Miru *NEW*