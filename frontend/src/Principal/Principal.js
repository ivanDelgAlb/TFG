import React from "react";
import './Principal.css'

export default function Principal() {
    return(
        <>
            <div className="container">
                <div className="bar">
                    <h1 className="title">TFG project</h1>
                </div>
                <div className="description">
                    <p>
                        The aim of this page is to provide a tool to determine when is expected
                        for a quantum machine to perform better and depending on the characteristics of the circuit
                        when it will be better to execute it.
                    </p>
                    <p>
                        We are both finishing our studies of Software Engineering in the university of Málaga and this
                        is part of our final project for the degree.
                    </p>
                </div>
            </div>
        </>
    )
}