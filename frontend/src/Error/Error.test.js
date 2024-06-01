import React from 'react'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import Error from './Error'

jest.mock('jest-fetch-mock')

beforeEach(() => {
    fetch.resetMocks()
})

describe('Error Component', () => {
    test('renders without crashing', () => {
        render(<Error />);
        expect(screen.getByText(/Prediction within a Date Range/i)).toBeInTheDocument()

        const machineInput = screen.getByLabelText('Select a machine')
        expect(machineInput).toBeInTheDocument()

        const optionInput = screen.getByLabelText('Select an option')
        expect(optionInput).toBeInTheDocument()

        const datePicker = screen.getByLabelText(/selected date/i)
        expect(datePicker).toBeInTheDocument()

        const modelInput = screen.getByLabelText('Select a model')
        expect(modelInput).toBeInTheDocument()
    })

    test('shows error message when fields are missing', async () => {
        render(<Error />)

        fireEvent.click(screen.getByText(/Submit/i));
        
        await waitFor(() => {
            expect(screen.getByText(/All fields are required/i)).toBeInTheDocument()
        })
    })

    test('shows error message when date is not the future', async () => {
        render(<Error />)

        fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
        fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Gates' } });
        fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });


        const pastDate = new Date()
        pastDate.setDate(pastDate.getDate() - 1)
        
        const calendarIcon = screen.getByLabelText('selected date')
        fireEvent.click(calendarIcon);

        fireEvent.click(screen.getByText(/Submit/i));

        await waitFor(() => {
            expect(screen.getByText(/Selected date must be after the current date/i)).toBeInTheDocument()
        })
    })

    test('shows graphics when the form is submitted correctly', async () => {
        render(<Error />);

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
    
        fireEvent.change(screen.getByLabelText(/Select a machine/i), { target: { value: 'ibm Brisbane' } });
        fireEvent.change(screen.getByLabelText(/Select an option/i), { target: { value: 'Qubits' } });
        fireEvent.change(screen.getByLabelText(/Select a model/i), { target: { value: 'Perceptron' } });
        fireEvent.change(screen.getByLabelText(/Select a depth/i), { target: { value: 5 } });
        fireEvent.change(screen.getByLabelText(/nQubitsInput/i), { target: { value: 2 } });
        fireEvent.change(screen.getByLabelText(/tGatesInput/i), { target: { value: 2 } });
        fireEvent.change(screen.getByLabelText(/phaseGatesInput/i), { target: { value: 2 } });
        fireEvent.change(screen.getByLabelText(/hGatesInput/i), { target: { value: 2 } });
        fireEvent.change(screen.getByLabelText(/cGatesInput/i), { target: { value: 2 } });
    
        const calendarIcon = screen.getByLabelText('selected date');
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