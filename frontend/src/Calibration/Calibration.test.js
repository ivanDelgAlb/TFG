import React from "react";
import Calibration from "./Calibration2"
import { fireEvent, render, screen, waitFor } from "@testing-library/react";

describe('Calibration Component', () => {

    test('renders without crashing', () => {
        render(<Calibration/>);

        expect(screen.getByText(/Noise prediction of a calibration/i)).toBeInTheDocument();

        const optionSelector = screen.getByText(/Select an option/i)
        expect(optionSelector).toBeInTheDocument()

        const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
        expect(nQubitsInput).toBeInTheDocument()

        const tGates = screen.getByLabelText(/tGatesInput/i)
        expect(tGates).toBeInTheDocument()

        const phaseGatesInput = screen.getByLabelText(/phaseGatesInput/i)
        expect(phaseGatesInput).toBeInTheDocument()

        const hGatesInput = screen.getByLabelText(/hGatesInput/i)
        expect(hGatesInput).toBeInTheDocument()

        const cGatesInput = screen.getByLabelText(/cGatesInput/i)
        expect(cGatesInput).toBeInTheDocument()

        const fileInput = screen.getByLabelText(/fileInput/i)
        expect(fileInput).toBeInTheDocument()
    })

    describe('shows error', () => {
        test('when the option is missing', async () => {
            render(<Calibration/>);
    
            fireEvent.click(screen.getByText(/Submit/i))
    
            await waitFor(() => {
                expect(screen.getByText(/You must select an option/i)).toBeInTheDocument()
            })
        })

        test('when the depth is missing', async () => {
            render(<Calibration/>);

            const optionSelector = screen.getByLabelText(/optionSelector/i)
            fireEvent.change(optionSelector, {target: {value: "Qubits"}})
    
            fireEvent.click(screen.getByText(/Submit/i))
    
            await waitFor(() => {
                expect(screen.getByText(/You must select a depth/i)).toBeInTheDocument()
            })
        })

        test('when the number of qubits is missing', async () => {
            render(<Calibration/>);

            const optionSelector = screen.getByLabelText(/optionSelector/i)
            fireEvent.change(optionSelector, {target: {value: "Qubits"}})

            const depthSelector = screen.getByLabelText(/depthSelector/i)
            fireEvent.change(depthSelector, {target: {value: "5"}})
    
            fireEvent.click(screen.getByText(/Submit/i))
    
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of qubits/i)).toBeInTheDocument()
            })
        })

        test('when the number of T gates is missing', async () => {
            render(<Calibration/>);

            const optionSelector = screen.getByLabelText(/optionSelector/i)
            fireEvent.change(optionSelector, {target: {value: "Gates"}})

            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})
    
            fireEvent.click(screen.getByText(/Submit/i))
    
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of T gates/i)).toBeInTheDocument()
            })
        })

        test('when the number of phase gates is missing', async () => {
            render(<Calibration/>);

            const optionSelector = screen.getByLabelText(/optionSelector/i)
            fireEvent.change(optionSelector, {target: {value: "Gates"}})

            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})

            const tGates = screen.getByLabelText(/tGatesInput/i)
            fireEvent.change(tGates, {target: {value: 1}})
    
            fireEvent.click(screen.getByText(/Submit/i))
    
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of phase gates/i)).toBeInTheDocument()
            })
        })

        test('when the number of Hadamard gates is missing', async () => {
            render(<Calibration/>);

            const optionSelector = screen.getByLabelText(/optionSelector/i)
            fireEvent.change(optionSelector, {target: {value: "Gates"}})

            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})

            const tGates = screen.getByLabelText(/tGatesInput/i)
            fireEvent.change(tGates, {target: {value: 1}})

            const phaseGatesInput = screen.getByLabelText(/phaseGatesInput/i)
            fireEvent.change(phaseGatesInput, {target: {value: 1}})
    
            fireEvent.click(screen.getByText(/Submit/i))
    
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of Hadamard gates/i)).toBeInTheDocument()
            })
        })

        test('when the number of CNot gates is missing', async () => {
            render(<Calibration/>);

            const optionSelector = screen.getByLabelText(/optionSelector/i)
            fireEvent.change(optionSelector, {target: {value: "Gates"}})

            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})

            const tGates = screen.getByLabelText(/tGatesInput/i)
            fireEvent.change(tGates, {target: {value: 1}})

            const phaseGatesInput = screen.getByLabelText(/phaseGatesInput/i)
            fireEvent.change(phaseGatesInput, {target: {value: 1}})

            const hGatesInput = screen.getByLabelText(/hGatesInput/i)
            fireEvent.change(hGatesInput, {target: {value: 1}})
    
            fireEvent.click(screen.getByText(/Submit/i))
    
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of C-Not gates/i)).toBeInTheDocument()
            })
        })
    
        test('when calibration file is missing', async () => {
            render(<Calibration/>);
    
            const optionSelector = screen.getByLabelText(/optionSelector/i)
            fireEvent.change(optionSelector, {target: {value: "Qubits"}})
    
            const depthSelector = screen.getByLabelText(/depthSelector/i)
            fireEvent.change(depthSelector, {target: {value: "5"}})
    
            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})
    
            const tGates = screen.getByLabelText(/tGatesInput/i)
            fireEvent.change(tGates, {target: {value: 1}})
    
            const phaseGatesInput = screen.getByLabelText(/phaseGatesInput/i)
            fireEvent.change(phaseGatesInput, {target: {value: 1}})
    
            const hGatesInput = screen.getByLabelText(/hGatesInput/i)
            fireEvent.change(hGatesInput, {target: {value: 1}})
    
            const cGatesInput = screen.getByLabelText(/cGatesInput/i)
            fireEvent.change(cGatesInput, {target: {value: 1}})
    
            fireEvent.click(screen.getByText(/Submit/i))
    
            await waitFor(() => {
                expect(screen.getByText(/You must submit a configuration file/i)).toBeInTheDocument()
            })
        })

        test('when the file is not a json', async () => {
            render(<Calibration/>);
    
            const optionSelector = screen.getByLabelText(/optionSelector/i)
            fireEvent.change(optionSelector, {target: {value: "Qubits"}})
    
            const depthSelector = screen.getByLabelText(/depthSelector/i)
            fireEvent.change(depthSelector, {target: {value: "5"}})
    
            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})
    
            const tGates = screen.getByLabelText(/tGatesInput/i)
            fireEvent.change(tGates, {target: {value: 1}})
    
            const phaseGatesInput = screen.getByLabelText(/phaseGatesInput/i)
            fireEvent.change(phaseGatesInput, {target: {value: 1}})
    
            const hGatesInput = screen.getByLabelText(/hGatesInput/i)
            fireEvent.change(hGatesInput, {target: {value: 1}})
    
            const cGatesInput = screen.getByLabelText(/cGatesInput/i)
            fireEvent.change(cGatesInput, {target: {value: 1}})
    
            const dummyFile = new File(['Dummy content'], 'example.pdf', { type: 'application/pdf' });
            const fileInput = screen.getByLabelText(/fileInput/i);

            const fileChangeEvent = new Event('change', { bubbles: true });
            Object.defineProperty(fileInput, 'files', {
                value: [dummyFile],
            });
            fireEvent(fileInput, fileChangeEvent);
    
            await waitFor(() => {
                expect(screen.getByText(/The configuration file must be a JSON/i)).toBeInTheDocument()
            })
        })
    })

    test('starts processing when the fields are submitted correctly', async () => {
        render(<Calibration/>);

        const optionSelector = screen.getByLabelText(/optionSelector/i)
        fireEvent.change(optionSelector, {target: {value: "Qubits"}})

        const depthSelector = screen.getByLabelText(/depthSelector/i)
        fireEvent.change(depthSelector, {target: {value: "5"}})

        const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
        fireEvent.change(nQubitsInput, {target: {value: 1}})

        const tGates = screen.getByLabelText(/tGatesInput/i)
        fireEvent.change(tGates, {target: {value: 1}})

        const phaseGatesInput = screen.getByLabelText(/phaseGatesInput/i)
        fireEvent.change(phaseGatesInput, {target: {value: 1}})

        const hGatesInput = screen.getByLabelText(/hGatesInput/i)
        fireEvent.change(hGatesInput, {target: {value: 1}})

        const cGatesInput = screen.getByLabelText(/cGatesInput/i)
        fireEvent.change(cGatesInput, {target: {value: 1}})

        const dummyFile = new File(['Dummy content'], 'example.json', { type: 'application/json' });
            const fileInput = screen.getByLabelText(/fileInput/i);

            const fileChangeEvent = new Event('change', { bubbles: true });
            Object.defineProperty(fileInput, 'files', {
                value: [dummyFile],
            });
            fireEvent(fileInput, fileChangeEvent);

        fireEvent.click(screen.getByText(/Submit/i))

        await waitFor(() => {
            expect(screen.getByText(/Loading.../i)).toBeInTheDocument()
        })
    })

    
})