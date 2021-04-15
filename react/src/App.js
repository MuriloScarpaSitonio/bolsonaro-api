import React, { useEffect, useState } from "react"
import { Container } from "react-bootstrap"
import { BrowserRouter as Router, Switch, Route } from "react-router-dom"

import { Contribute } from "./components/common/Contribute"
import Error from "./components/static/Error"
import Footer from "./components/static/Footer"
import Home from "./components/common/Home"
import EntityHome from "./components/entity/EntityHome"
import EntityQuery from "./components/entity/EntityQuery"
import Entity from "./components/entity/Entity"
import MetaData from "./components/MetaData"
import LegalInfos from "./components/static/LegalInfos"
import Navbar from "./components/common/Navbar"

import bozoQuote from "./images/bozoQuote.png"
import bozoAction from "./images/bozoAction.png"

import './App.scss'

const useDarkMode = () => {
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

const Wrapper = (props) => {
  const [theme, themeToggler] = useDarkMode()

  return (
        <div className={theme}>
          <div className='base'>
            <Container>
              <MetaData />
              <Navbar themeToggler={themeToggler}/>
              <props.component {...props} />
              <br />
              <br />
              <Footer />
            </Container>
          </div>
        </div>
    )
  }


export default function App() {
  return (
    <Router>
      <Switch>
        <Route exact path="/"
          render={props => (
            <Wrapper {...props} component={Home} />
          )}
        />
        <Route exact path="/legal-infos"
          render={props => (
            <Wrapper {...props} component={LegalInfos} />
          )}
        />
        <Route
          exact path="/actions"
          key="action-home"
          render={props => (
            <Wrapper
              {...props}
              image={bozoAction}
              baseEndpoint="actions"
              component={EntityHome}
            />
          )}
        />
        <Route
          path="/actions/query"
          key="action-query"
          render={props => (
            <Wrapper
              {...props}
              image={bozoAction}
              baseEndpoint="actions"
              component={EntityQuery}
            />
          )}
        />
        <Route
          path="/actions/:id(\d+)"
          key="action-entity"
          render={props => (
            <Wrapper
              {...props}
              image={bozoAction}
              baseEndpoint="actions"
              component={Entity}
            />
          )}
        />
        <Route
          exact path="/quotes"
          key="quote-home"
          render={props => (
            <Wrapper
              {...props}
              image={bozoQuote}
              baseEndpoint="quotes"
              component={EntityHome}
            />
          )}
        />
        <Route
          path="/quotes/query"
          key="quote-query"
          render={props => (
            <Wrapper
              {...props}
              image={bozoQuote}
              baseEndpoint="quotes"
              component={EntityQuery}
            />
          )}
        />
        <Route
          path="/quotes/:id(\d+)"
          key="quote-entity"
          render={props => (
            <Wrapper
              {...props}
              image={bozoQuote}
              baseEndpoint="quotes"
              component={Entity}
            />
          )}
        />
        <Route exact path="/contribute"
          render={props => (
            <Wrapper {...props} component={Contribute} />
          )} />
        <Route render={props => (
          <Wrapper
            {...props}
            message={"Página não encontrada!"}
            badRequest={true}
            component={Error}
          />
        )}
        />
      </Switch>
    </Router>
  )
}
