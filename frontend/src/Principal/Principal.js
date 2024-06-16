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
                            <p>Calculate when it will be better for your circuit to be executed.</p>
                        </div>
                        <div className="feature-item" onClick={() => window.location.href = '/calibration'}>
                            <h3>Custom Calibrations</h3>
                            <p>Predict the error of a circuit with your custom calibration by uploading JSON files.</p>
                        </div>
                        <div className="feature-item" onClick={() => window.location.href = '/historical'}>
                            <h3>Historical Data</h3>
                            <p>Analyze the historical calibrations of the machines.</p>
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
                    <div>
                        <a href="https://github.com/marinasayago" style={{ textDecoration: 'none', color: 'inherit' }}>
                            <img 
                            src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" 
                            alt="GitHub" 
                            width="20" 
                            height="20" 
                            style={{ verticalAlign: 'middle', marginRight: '8px' }} 
                            />
                            Marina Sayago Gutiérrez
                        </a>
                    </div>
                    <div>
                        <a href="https://github.com/IvanUma" style={{ textDecoration: 'none', color: 'inherit' }}>
                            <img 
                            src="https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png" 
                            alt="GitHub" 
                            width="20" 
                            height="20" 
                            style={{ verticalAlign: 'middle', marginRight: '8px' }} 
                            />
                            Iván Delgado Alba
                        </a>
                    </div>

                </section>
            </main>
        </>
    );
}
