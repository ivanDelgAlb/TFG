import React from "react";
import './Principal.css';

export default function Principal() {
    return (
        <>
            <main className="main-content">
                <section className="intro">
                    <h2>Optimize Your Quantum Computing Tasks</h2>
                    <p>
                        Discover the best times to run your quantum algorithms with our advanced prediction tool.
                        Make informed decisions based on real-time data and enhance the performance of your quantum machine.
                    </p>
                    <button className="explore-button" onClick={() => window.location.href = '#features'}>Explore Features</button>
                </section>
                <section id="features" className="features">
                    <h2>Features</h2>
                    <div className="feature-list">
                        <div className="feature-item" onClick={() => window.location.href = '/error'}>
                            <h3>Error Calculation</h3>
                            <p>Calculate errors for various dates and parameters.</p>
                        </div>
                        <div className="feature-item" onClick={() => window.location.href = '/calibration'}>
                            <h3>Custom Calibrations</h3>
                            <p>Input custom calibrations or upload JSON files.</p>
                        </div>
                        <div className="feature-item" onClick={() => window.location.href = '/historical'}>
                            <h3>Historical Data</h3>
                            <p>Analyze the historical performance of your machines.</p>
                        </div>
                    </div>
                </section>
                <section id="about" className="about">
                    <h2>About Us</h2>
                    <p>
                        We are two students cursing our final year of Software Engineering at the University of Málaga.
                        This application is part of our final degree project, aimed at improving the efficiency of quantum computing by providing a tool to predict whenever an execution of a circuit will be more reliable.
                    </p>
                </section>
                <section id="contact" className="contact">
                    <h2>Contact Us</h2>
                    <p>If you have any questions or feedback, feel free to reach out!</p>
                </section>
            </main>
        </>
    );
}
