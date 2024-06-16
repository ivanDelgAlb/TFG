import React from "react";
import Historical from "./Historical";
import { fireEvent, render, screen } from "@testing-library/react";
import { act } from "react";

describe('Historical Component', () => {
    
  test('renders without crashing', async () => {
    render(<Historical/>);

    expect(screen.getByText(/Historical/i)).toBeInTheDocument();

    const brisbaneButton = screen.getByText('ibm Brisbane');
    expect(brisbaneButton).toBeInTheDocument();

    const kyotoButton = screen.getByText('ibm Kyoto');
    expect(kyotoButton).toBeInTheDocument();

    const osakaButton = screen.getByText('ibm Osaka');
    expect(osakaButton).toBeInTheDocument();
  });

  test('starts processing when an option is selected', async () => {
    render(<Historical/>);

    const brisbaneButton = screen.getByText('ibm Brisbane');

    act(() => {
        fireEvent.click(brisbaneButton);
    })

    expect(screen.getByText('All the historical data')).toBeInTheDocument();

    fireEvent.change(screen.getByText('All the historical data'), { target: { value: 'Qubits' } });
    fireEvent.click(screen.getByText(/Show Calibration Charts/i));

    expect(screen.getByText('Hide Calibration Charts')).toBeInTheDocument()
  });
});
