import { useEffect, useState } from "react"

import { BASE_API_URL } from "../consts"


export const useQuery = (url, shouldFetch = true, setShouldFetch = null) => {
    const [data, setData] = useState({})
    const [isLoaded, setIsLoaded] = useState(false)
    const [error, setError] = useState(null)
    
    useEffect(() => {
        if(shouldFetch) {
            fetch(`${BASE_API_URL}/${url}`)
                .then(response => {
                    if(!response.ok) {
                        response.json().then(error => setError({message: error.errorMessage,badRequest: true}))
                    }
                    else {
                        response.json().then(
                            data => {
                                setData(data)
                                setIsLoaded(true)
                                if (setShouldFetch) setShouldFetch(false)
                            },
                            error => {
                                setError(error)
                                setIsLoaded(true)
                            }
                                
                        )
                    }
                })
                .catch(error => {
                    setError(error)
                    setIsLoaded(true)
                })
        }
        }, [url, shouldFetch, setShouldFetch])
    return [data, isLoaded, error]
};


export const useAsyncQuery = (urls) => {
    const [data, setData] = useState([])
    const [isLoaded, setIsLoaded] = useState(false)
    const [error, setError] = useState(null)
    
    useEffect(() => {
        Promise.all(urls.map(url => fetch(`${BASE_API_URL}/${url}`)))
            .then(responses => Promise.all(responses.map(response => response.json())))
            .then(
                data => {
                    setData(data)
                    setIsLoaded(true)
                },
                error => {
                    setError(error)
                    setIsLoaded(true)
                }
            )
            .catch(error => {
                setError(error)
                setIsLoaded(true)
            })
        }, [])
    return [data, isLoaded, error]
  };