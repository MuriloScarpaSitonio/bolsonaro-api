import React, { useState} from 'react'

import { useHistory } from 'react-router-dom'
import HomeIcon from '@material-ui/icons/Home'
import WbSunnyIcon from '@material-ui/icons/WbSunny'
import NightsStayIcon from '@material-ui/icons/NightsStay'
import IconButton from '@material-ui/core/IconButton'
import MenuIcon from '@material-ui/icons/Menu'
import SearchIcon from '@material-ui/icons/Search'
import { Button, Form, InputGroup, Navbar } from 'react-bootstrap'

import { getVariant } from '../helpers'

import './Navbar.scss'

const NavBar = (props) => {
    let history = useHistory()
    const [open, setOpen] = useState(false)
    const [dark, setDark] = useState(window.localStorage.getItem('theme') === 'theme--dark')
    
    const onClick = () => {
        props.themeToggler()
        setDark(!dark)
    }
       
    const handleSubmit = (e) => {
        e.preventDefault()
        let baseEndpoint = e.target[1].value === 'Ações' ? 'actions' : 'quotes'
        history.push({
            pathname: `/${baseEndpoint}/query`,
            search: `?description=${e.target[0].value}`, 
        })
    }

    return (
        <>
            <Navbar className={`custom-navbar ${open ? 'open' : ''}`} expand='sm' sticky='top'>
                <Navbar.Toggle
                    id='toggler'
                    className='text-right'
                    aria-controls='navbar-collapse'
                    onClick={() => setOpen(!open)}
                >
                    <MenuIcon className='custom-navbar__icon' />
                </Navbar.Toggle>
                <IconButton onClick={() => history.push('/')}>
                    <HomeIcon className='custom-navbar__icon' />
                </IconButton>
                <Navbar.Collapse id='navbar-collapse'>
                    <div id='custom-navbar__form-container'>
                        <Form inline onSubmit={handleSubmit} className='d-flex justify-content-center'>
                            <InputGroup id='custom-navbar__input-group'>
                                <Form.Control
                                    id='custom-navbar__search-input'
                                    placeholder='Pesquise'
                                    type='search'
                                    size='sm'
                                />
                                <Form.Control as='select' size='sm'>
                                    <option>Ações</option>
                                    <option>Declarações</option>
                                </Form.Control>
                                <InputGroup.Append >
                                    <Button
                                        id='custom-navbar__search-button'
                                        size='sm'
                                        type='submit'
                                        variant={'outline-' + getVariant()}
                                    >
                                        <SearchIcon id='custom-navbar__search-icon' fontSize='small' />
                                    </Button>
                                </InputGroup.Append>
                            </InputGroup>  
                        </Form>
                    </div>
                </Navbar.Collapse>
                <IconButton onClick={onClick}>
                    {dark ?
                        <NightsStayIcon className='custom-navbar__icon' /> :
                        <WbSunnyIcon className='custom-navbar__icon' />
                    }
                </IconButton>
            </Navbar>
            <div className={`overlay ${open ? 'open' : ''}`} />
        </>
    )
}

export default NavBar