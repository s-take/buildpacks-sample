# buildpackチュートリアル

## 事前準備

以下をインストールしておく
- docker
- pack

## stack作成

- build imageとrun imageのDockerfileを作成し、それぞれ(ローカル)ビルドする

```
cd stacks
docker build -t distroless-python:run -f ./distroless-python/run/Dockerfile .
docker build -t distroless-python:build -f ./distroless-python/build/Dockerfile .
```

- 成功してたらローカルにイメージできてる

```
docker images |grep distro
distroless-python                     build                                                   c86408d3b964   12 seconds ago   113MB
distroless-python                     run                                                     82082a1289c9   51 years ago     52.2MB
```

## buildpack作成

- buildpackに必要な以下の３ファイルを作成する
  - buildpack.toml
  - bin/detect
  - bin/build

## builder作成

- builder.tomlを作成し、buildpacks,stacksの情報を記載する
  - buildpacksはdockerイメージでも可能
- 作成したらpackでbuilderを作成する

```
cd builders
pack builder create python:distroless --config ./distroless-python/builder.toml
```

## app image作成

```
pack build empty-sample --builder python:distroless
```

### buildpack追加

イメージ作成後にbuildpackを作成する場合、2つ手法がある
1. buildpack追加後にbuilder自体を再作成する(builder.toml修正が必要)
2. buildpackを指定してpack buildする

1は上記手順を繰り返すだけなので2の手順だけ記載

```
cd sample-app
pack build webapp --builder python:distroless --buildpack ../buildpacks/python
```

## 参考

- [Buildpacksのビルダーをスクラッチから作ってみる](https://future-architect.github.io/articles/20201002/)