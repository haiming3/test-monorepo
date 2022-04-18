/**
* major: A code change that can upgrade the major version
* feat: A new feature
* data: Data update
* fix: A bug fix
* enh: Code enhancement
* refactor: A code change that neither fixes a bug nor adds a feature
* perf: A code change that improves performance
* chore: Changes to the build process or auxiliary tools and libraries such as documentation generation
* test: Adding missing or correcting existing tests
* docs: Documentation only changes
*/
module.exports = {
  extends: [
    '@commitlint/config-conventional'
  ],
  parserPreset: {
    parserOpts: {
      issuePrefixes: ['https://app.asana.com/', 'no_tas']
    }
  },
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'data', 'fix', 'enh', 'refactor', 'perf', 'chore', 'test', 'docs', 'major'
    ]],
    'type-empty': [2, 'never'],
    'type-case': [0],
    'scope-enum': [2, 'always', [
      'common', 'all', 'zoom', 'wechat', 'hisense', 'windquiet', 'triage', 'ucrest', 'coinbase', 'chime', 'new'
    ]],
    'scope-empty': [2, 'never'],
    'scope-case': [0],
    'subject-full-stop': [0, 'never'],
    'subject-case': [0, 'never'],
    'subject-empty': [2, 'never'],
    'subject-min-length': [0, 'always', 10],
    'references-empty': [2, 'never'],
    'header-max-length': [0, 'always', 72]
  },
  plugins: [
    'commitlint-plugin-subject-references'
  ]
}