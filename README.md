Пример кода:
```python
def test(self,prompt, path = "D:/Tor Browser/Browser/", headless = False, browser = "firefox1.exe", model = "GPT-4o"):
    DT = DuckChat_Tor(path, headless, "https://duckduckgo.com/?q=DuckDuckGo+AI+Chat&ia=chat&duckai=1", browser = browser, service= "D:/geckodriver.exe", model = model)
    return DT.GetPrompt(prompt)
```
