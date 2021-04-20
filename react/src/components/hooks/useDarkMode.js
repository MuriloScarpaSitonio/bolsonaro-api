import { useEffect, useState } from "react"

export const useDarkMode = () => {
    const [theme, setTheme] = useState('theme--light')
    
    const setMode = mode => {
        window.localStorage.setItem('theme', mode)
        setTheme(mode)
    }
  
    const themeToggler = () => theme === 'theme--light' ? setMode('theme--dark') : setMode('theme--light')
  
    useEffect(() => {
        const localTheme = window.localStorage.getItem('theme')
        localTheme && setTheme(localTheme)
    }, [])
    return [theme, themeToggler]
  };