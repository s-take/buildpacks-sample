# buildpackチュートリアル

stack作成〜rebaseまでを体験

## 事前準備

以下をインストールしておく
- docker
- pack

## Stack/Buildpack/Builder作成

![](https://buildpacks.io/docs/concepts/components/create-builder.svg)

### stack作成

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

### buildpack作成

- 以下のようなコマンドでディレクトリを作成する（今回はすでに作成済み）

```
pack buildpack new examples/ruby \
    --api 0.5 \
    --path ruby-buildpack \
    --version 0.0.1 \
    --stacks io.buildpacks.samples.stacks.bionic
```

- buildpackに必要な以下の３ファイルを作成する
  - buildpack.toml
  - bin/detect
  - bin/build

### 番外: buildpackのレジストリ登録

buildpackをOCIイメージとして登録する方法。以下の手順が必要
1. buildpackのパッケージ化  
- package.tomlを作成し、idやdependenciesを定義する
- 以下の例だとmy-buildpackのdockerイメージとして生成される
```
cd packages
pack buildpack package example/my-cnb --config ./empty/package.toml
```

2. buildpackのレジストリ登録  
- docker hubにpushする
```
docker push example/my-cnb
```
- この情報を元に本家buildpackに登録。以下の例だと example/my-cnb という名前で登録される
- ここでgithub認証が出るが本当に登録する予定がないため実施していない
```
pack buildpack register example/my-cnb
```

### builder作成

- builder.tomlを作成し、buildpacks,stacksの情報を記載する
  - 今回buildpackはディレクトリ指定だが、dockerイメージでも可能
- 作成したらpackでbuilderを作成する

```
cd builders
pack builder create python:distroless --config ./distroless-python/builder.toml
```

## app image作成

![](https://buildpacks.io/docs/concepts/operations/build.svg)

```
cd sample-app
pack build webapp --builder python:distroless
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

## rebase

![](https://buildpacks.io/docs/concepts/operations/rebase.svg)

```
cd stacks
vi ./distroless-python/run/Dockerfile
docker build -t distroless-python:run -f ./distroless-python/run/Dockerfile .
```

更新後にrebase実行する

```
pack rebase 
```

## 参考

- [Buildpacksのビルダーをスクラッチから作ってみる](https://future-architect.github.io/articles/20201002/)