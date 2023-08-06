# Gnome Extension Uploader
Tool to upload Gnome-Shell extensions to [extensions.gnome.org](https://extensions.gnome.org).

## Install
```console
pip install gnome-extension-uploader
```

## How to use
```console
geu build # runs glib-compile-schemas and builds the zip file
geu publish --username <YOUR_EXTENSIONS_GNOME_ORG_USERNAME> --password <YOUR_EXTENSIONS_GNOME_ORG_PASSWORD>
geu --help # for help :)
```

You can also provide your username and password via environment variables (GEU_USERNAME, GEU_PASSWORD).

## Use in Gitlab CI/CD
Add GEU_USERNAME and GEU_PASSWORD to your build variables in your repository settings.

This will publish every tag on [extensions.gnome.org](https://extensions.gnome.org)
```yaml
stages:
  - publish

production:
  image: python:3.8.3-buster
  stage: publish
  script:
    - pip install gnome-extension-uploader
    - geu publish
  only:
    - tags
```

## Support
Feel free to submit a pull request or consider making a donation on [Flatter](https://flattr.com/@SebastianNoelLuebke).