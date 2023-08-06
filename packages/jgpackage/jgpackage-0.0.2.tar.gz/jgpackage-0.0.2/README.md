# jgpackage

Este é um pacote mínimo que serve como tutorial para:
* deploy de pacotes no PyPi
* uso de pipelines CI\CD para Python Packages

## Como usar:
```shell script
pip install jgpackage
```
And to use the package:

```python
>>> import samplePackage as sp
>>> sp.format_text("Yolo")
'my input: Yolo'
```

## Read the \_\_doc__
> One of Guido's key insights is that code is read much more often than it is written.
> [PEP8](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds)

Então, seguem algumas dicas para ler a documentação do pacote.

1. Help
```python
>>> import samplePackage as sp
>>> help(sp) #help no módulo
>>> help(sp.format_text) #help na função
```
2. \_\_doc__
```python
>>> print(sp.__doc__) #doc do modulo
>>> print(sp.format_text.__doc__) #doc da função
```