import React from 'react'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import Error from './Error'
import fs from 'fs'

jest.mock('jest-fetch-mock')

beforeEach(() => {
    fetch.resetMocks()
})

function getDaySuffix(day) {
    if (day >= 11 && day <= 13) {
        return 'th';
    }
    switch (day % 10) {
        case 1: return 'st';
        case 2: return 'nd';
        case 3: return 'rd';
        default: return 'th';
    }
}

describe('Error Component', () => {
    test('renders without crashing', () => {
        render(<Error />);
        expect(screen.getByText(/Prediction within a Date Range/i)).toBeInTheDocument()

        const machineInput = screen.getByLabelText(/Select a machine/i)
        expect(machineInput).toBeInTheDocument()

        const optionInput = screen.getByLabelText(/Select an option/i)
        expect(optionInput).toBeInTheDocument()

        const datePicker = screen.getByLabelText(/selected date/i)
        expect(datePicker).toBeInTheDocument()

        const modelInput = screen.getByLabelText(/Select a model/i)
        expect(modelInput).toBeInTheDocument()
    })

    describe('shows error', () => {

        test('when machine is missing', async () => {
            render(<Error />)
    
            fireEvent.click(screen.getByText(/Submit/i));
            
            await waitFor(() => {
                expect(screen.getByText(/You must select a machine/i)).toBeInTheDocument()
            })
        })

        test('when option is missing', async () => {
            render(<Error />)

            fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
    
            fireEvent.click(screen.getByText(/Submit/i));
            
            await waitFor(() => {
                expect(screen.getByText(/You must select an option/i)).toBeInTheDocument()
            })
        })

        test('when model is missing', async () => {
            render(<Error />)

            fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
            fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Gates' } });

            const calendarIcon = screen.getByLabelText(/selected date/i);
            fireEvent.click(calendarIcon);
        
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
            const daysOfTheWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            const day = daysOfTheWeek[tomorrow.getDay()];
            const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            const month = months[tomorrow.getMonth()];
            const year = tomorrow.getFullYear();
            const daySuffix = getDaySuffix(tomorrow.getDate());
            const text = `Choose ${day}, ${month} ${tomorrow.getDate()}${daySuffix}, ${year}`;
            const futureDate = screen.getByLabelText(text);

            fireEvent.click(futureDate);

            fireEvent.click(screen.getByText(/Submit/i));
            
            await waitFor(() => {
                expect(screen.getByText(/You must select a model/i)).toBeInTheDocument()
            })
        })

        test('when depth is missing', async () => {
            render(<Error />)

            fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
            fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Qubits' } });
            fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });

            fireEvent.click(screen.getByText(/Submit/i));
            
            await waitFor(() => {
                expect(screen.getByText(/You must select a depth/i)).toBeInTheDocument()
            })
        })

        test('when the number of qubits is missing', async () => {
            render(<Error />)

            fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
            fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Gates' } });
            fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });

            fireEvent.click(screen.getByText(/Submit/i));
            
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of qubits/i)).toBeInTheDocument()
            })
        })

        test('when the number of T gates is missing', async () => {
            render(<Error />)

            fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
            fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Gates' } });
            fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });
            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})

            fireEvent.click(screen.getByText(/Submit/i));
            
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of T gates/i)).toBeInTheDocument()
            })
        })

        test('when the number of phase gates is missing', async () => {
            render(<Error />)

            fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
            fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Gates' } });
            fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });

            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})

            const tGates = screen.getByLabelText(/tGatesInput/i)
            fireEvent.change(tGates, {target: {value: 1}})

            fireEvent.click(screen.getByText(/Submit/i));
            
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of phase gates/i)).toBeInTheDocument()
            })
        })

        test('when the number of Hadamard gates is missing', async () => {
            render(<Error />)

            fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
            fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Gates' } });
            fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });

            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})

            const tGates = screen.getByLabelText(/tGatesInput/i)
            fireEvent.change(tGates, {target: {value: 1}})

            const phaseGatesInput = screen.getByLabelText(/phaseGatesInput/i)
            fireEvent.change(phaseGatesInput, {target: {value: 1}})

            fireEvent.click(screen.getByText(/Submit/i));
            
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of Hadamard gates/i)).toBeInTheDocument()
            })
        })

        test('when the number of cNot gates is missing', async () => {
            render(<Error />)

            fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
            fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Gates' } });
            fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });

            const nQubitsInput = screen.getByLabelText(/nQubitsInput/i)
            fireEvent.change(nQubitsInput, {target: {value: 1}})

            const tGates = screen.getByLabelText(/tGatesInput/i)
            fireEvent.change(tGates, {target: {value: 1}})

            const phaseGatesInput = screen.getByLabelText(/phaseGatesInput/i)
            fireEvent.change(phaseGatesInput, {target: {value: 1}})

            const hGatesInput = screen.getByLabelText(/hGatesInput/i)
            fireEvent.change(hGatesInput, {target: {value: 1}})

            fireEvent.click(screen.getByText(/Submit/i));
            
            await waitFor(() => {
                expect(screen.getByText(/You must select the number of C-Not gates/i)).toBeInTheDocument()
            })
        })

        test('when date is not the future', async () => {
            render(<Error />)
    
            fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
            fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Gates' } });
            fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });

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

            const calendarIcon = screen.getByLabelText(/selected date/i);
            fireEvent.click(calendarIcon);
        
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            const daysOfTheWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            const day = daysOfTheWeek[yesterday.getDay()];
            const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
            const month = months[yesterday.getMonth()];
            const year = yesterday.getFullYear();
            const daySuffix = getDaySuffix(yesterday.getDate());
            const text = `Choose ${day}, ${month} ${yesterday.getDate()}${daySuffix}, ${year}`;
            const futureDate = screen.getByLabelText(text);

            fireEvent.click(futureDate);
    
            fireEvent.click(screen.getByText(/Submit/i));
    
            await waitFor(() => {
                expect(screen.getByText(/Selected date must be after the current date/i)).toBeInTheDocument()
            })
        })

    })

    test('starts processing when the form is submitted correctly', async () => {
        render(<Error />);
    
        fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
        fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Gates' } });
        fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });

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
    
        const calendarIcon = screen.getByLabelText(/selected date/i);
        fireEvent.click(calendarIcon);
    
        const tomorrow = new Date();
        tomorrow.setDate(tomorrow.getDate() + 1);
        const daysOfTheWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const day = daysOfTheWeek[tomorrow.getDay()];
        const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
        const month = months[tomorrow.getMonth()];
        const year = tomorrow.getFullYear();
        const daySuffix = getDaySuffix(tomorrow.getDate());
        const text = `Choose ${day}, ${month} ${tomorrow.getDate()}${daySuffix}, ${year}`;
        const futureDate = screen.getByLabelText(text);
        fireEvent.click(futureDate);
    
        fireEvent.click(screen.getByText(/Submit/i));
    
        await waitFor(() => {
            expect(screen.getByText(/Loading.../i)).toBeInTheDocument();
        });

    });
})