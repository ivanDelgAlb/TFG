import React from "react";
import Historical from "./Historical";
import { fireEvent, render, screen } from "@testing-library/react";
import { act } from "react";

const mockFetch = (data) => {
  global.fetch = jest.fn().mockResolvedValue({
    json: jest.fn().mockResolvedValue(data),
  });
};

describe('Historical Component', () => {
  beforeEach(() => {
    mockFetch({
      'historical': [
        {
          'qubits': [{'Date': '2024-05-20 22:35:32', 'T1': 0.673757892838128, 'T2': 0.6577576748558496, 'probMeas0Prep1': 0.2142857142857108, 'probMeas1Prep0': 0.2916666666666652, 'readout_error': 0.1794871794871593}],
        },
        {
          'gates': [{'Date': '2024-05-20 22:35:32', 'gate_error_1': 0.2683540467997378, 'gate_error_2': 0.455328019849885}],
        },
        {
          'errorQubits': [{'Date': '2024-05-20 22:35:32', 'jensen-error': 0.1871445071468462}],
        },
        {
          'errorGates': [{'Date': '2024-05-20 22:35:32', 'jensen-error': 0.25003}],
        },
      ]
    });
  });
    
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

    expect(screen.getByText('Choose an option')).toBeInTheDocument();

    fireEvent.change(screen.getByText('Choose an option'), { target: { value: 'Qubits' } });
    fireEvent.click(screen.getByText(/Show Calibration Charts/i));

    expect(screen.getByText('Hide Calibration Charts')).toBeInTheDocument()
  });
});
