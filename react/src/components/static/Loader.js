import { Spinner } from "react-bootstrap"

import { getVariant } from "../helpers"

export const Loader = (props) => {
    return (
        <div className={"text-center " + (props.bootstrapClassName || "mt-5")}>
            <Spinner animation="border" variant={getVariant()} />
        </div>
    )
}
