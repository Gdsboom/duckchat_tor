Пример кода:
```python
async def test(prompt, path="D:/Tor Browser/Browser/", headless=False, browser="firefox.exe", model= "УДОБНАЯ ДЛЯ ВАС МОДЕЛЬ ИИ"):
    DT = DuckChat_Tor(path, headless, "https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1", browser=browser,
                      service="D:/geckodriver.exe", model=model)
    return (DT.GetPrompt(prompt))
```
