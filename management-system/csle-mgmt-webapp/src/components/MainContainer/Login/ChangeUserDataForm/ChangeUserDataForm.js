import React, {useState, useCallback} from 'react';
import {useAlert} from "react-alert";
import './Login.css';
import {useNavigate} from "react-router-dom";
import serverIp from "../../../Common/serverIp";
import serverPort from "../../../Common/serverPort";

/**
 * The component representing the /login-page
 */
const ChangeUserDataForm = (props) => {
    const [username, setUsername] = useState(props.sessionData.username);
    const [password, setPassword] = useState("");
    const [email, setEmail] = useState(props.sessionData.email);
    const [organization, setOrganization] = useState(props.sessionData.organization);
    const [firstName, setFirstName] = useState(props.sessionData.first_name);
    const [lastName, setLastName] = useState(props.sessionData.last_name);
    const [admin, setAdmin] = useState(props.sessionData.admin);
    const [userId, setUserId] = useState(props.sessionData.id);
    const [token, setToken] = useState(props.sessionData.token);
    const ip = serverIp
    const port = serverPort
    const alert = useAlert();
    const navigate = useNavigate();

    const updateUser = useCallback((user) => {
        fetch(
            `${HTTP_PREFIX}${ip}:${port}/` + ip + ':' + port + '/users/' + user.id + "?token=" + token,
            {
                method: "PUT",
                headers: new Headers({
                    Accept: "application/vnd.github.cloak-preview"
                }),
                body: JSON.stringify({user: user})
            }
        )
            .then(res => {
                if (res.status === 401) {
                    alert.show("Session token expired. Please login again.")
                    props.setSessionData(null)
                    navigate("/login-page");
                    return null
                }
                if (res.status === 400) {
                    alert.show("Invalid request, could not update user")
                    return null
                }
                return res.json()
            })
            .then(response => {
                var sessionData = {
                    "token" : props.sessionData.token,
                    "username": username,
                    "email": email,
                    "first_name": firstName,
                    "last_name": lastName,
                    "organization": organization,
                    "id": userId,
                    "admin": admin
                }
                props.setSessionData(sessionData)
                alert.show("User data updated successfully")
            })
            .catch(error => console.log("error:" + error))
    }, []);


    const updateUserFormSubmit = async (event) => {
        event.preventDefault()
        const userConfiguration = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": firstName,
            "last_name": lastName,
            "organization": organization,
            "id": userId,
            "admin": admin,
            "salt": ""
        }
        if (username === "" || password === "") {
            alert.show("Username or password cannot be empty")
        } else {
            updateUser(userConfiguration)
        }
    }

    const handleUsernameChange = (event) => {
        setUsername(event.target.value)
    }

    const handlePwChange = (event) => {
        setPassword(event.target.value)
    }

    const handleEmailChange = (event) => {
        setEmail(event.target.value)
    }

    const handleFirstNameChange = (event) => {
        setFirstName(event.target.value)
    }

    const handleLastNameChange = (event) => {
        setLastName(event.target.value)
    }

    const handleOrganizationChange = (event) => {
        setOrganization(event.target.value)
    }

    return (
        <div className="Login Auth-form-container">
            <form className="Auth-form" onSubmit={updateUserFormSubmit}>
                <div className="Auth-form-content">
                    <h3 className="Auth-form-title">User: {props.sessionData.username}</h3>
                    <div className="form-group mt-3">
                        <label>Admin rights</label>
                        <input
                            type="checkbox"
                            className="form-control mt-1 adminCheckbox"
                            placeholder="Admin rights (contact an administrator to change"
                            checked={admin}
                            disabled={true}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Username</label>
                        <input
                            type="username"
                            className="form-control mt-1"
                            placeholder="Enter username"
                            value={username}
                            onChange={handleUsernameChange}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Password</label>
                        <input
                            type="password"
                            className="form-control mt-1"
                            placeholder="Enter password"
                            value={password}
                            onChange={handlePwChange}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>First name</label>
                        <input
                            type="text"
                            className="form-control mt-1"
                            placeholder="Enter first name"
                            value={firstName}
                            onChange={handleFirstNameChange}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Last name</label>
                        <input
                            type="text"
                            className="form-control mt-1"
                            placeholder="Enter last name"
                            value={lastName}
                            onChange={handleLastNameChange}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>Organization</label>
                        <input
                            type="text"
                            className="form-control mt-1"
                            placeholder="Enter organization"
                            value={organization}
                            onChange={handleOrganizationChange}
                        />
                    </div>
                    <div className="form-group mt-3">
                        <label>E-mail</label>
                        <input
                            type="email"
                            className="form-control mt-1"
                            placeholder="Enter e-mail"
                            value={email}
                            onChange={handleEmailChange}
                        />
                    </div>
                    <div className="d-grid gap-2 mt-3">
                        <button type="submit" className="btn btn-primary">
                            Save changes
                        </button>
                    </div>
                </div>
            </form>
        </div>
    )
}

ChangeUserDataForm.propTypes = {};
ChangeUserDataForm.defaultProps = {};
export default ChangeUserDataForm;
