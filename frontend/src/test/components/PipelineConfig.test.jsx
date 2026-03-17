import { render, screen, fireEvent } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import PipelineConfig from '../../components/PipelineConfig/PipelineConfig';
import useDataStore from '../../stores/useDataStore';
import useAppStore from '../../stores/useAppStore';

// Mock the API so fetchPrepOptions doesn't hit a real backend
vi.mock('../../api', () => ({
  fetchPrepOptions: vi.fn(() => Promise.resolve({ data: null, error: 'mocked' })),
}));

describe('PipelineConfig', () => {
  let onApplyMock;

  beforeEach(() => {
    onApplyMock = vi.fn();

    useAppStore.setState({
      currentStep: 3,
      selectedDomainId: 'cardiology',
      showHelp: false,
    });
    useDataStore.setState({
      dataSource: 'default',
      csvData: null,
      csvFileName: null,
      csvError: null,
      targetColumn: null,
      columnMappings: {},
      mapperSaved: true,
      mapperOpen: false,
      pipelineConfig: {
        imputation: 'mean',
        scaling: 'minmax',
        trainTestSplit: 80,
        smote: false,
      },
      pipelineStatus: 'idle',
      pipelineProgress: 0,
      pipelineLogs: [],
      pipelineDuration: null,
      prepOptions: null,
    });
  });

  it('renders imputation dropdown with 4 options, default is mean', () => {
    render(<PipelineConfig onApply={onApplyMock} />);

    const imputationSelect = screen.getByLabelText(/missing value imputation/i);
    expect(imputationSelect.value).toBe('mean');

    const options = Array.from(imputationSelect.querySelectorAll('option'));
    expect(options).toHaveLength(4);

    const values = options.map((o) => o.value);
    expect(values).toContain('mean');
    expect(values).toContain('median');
    expect(values).toContain('mode');
    expect(values).toContain('drop');
  });

  it('renders scaling dropdown with 3 options, default is minmax', () => {
    render(<PipelineConfig onApply={onApplyMock} />);

    const scalingSelect = screen.getByLabelText(/feature scaling/i);
    expect(scalingSelect.value).toBe('minmax');

    const options = Array.from(scalingSelect.querySelectorAll('option'));
    expect(options).toHaveLength(3);

    const values = options.map((o) => o.value);
    expect(values).toContain('standard');
    expect(values).toContain('minmax');
    expect(values).toContain('none');
  });

  it('renders train/test slider with value 80, changing to 70 updates', async () => {
    render(<PipelineConfig onApply={onApplyMock} />);

    const slider = screen.getByRole('slider');
    expect(slider.value).toBe('80');

    fireEvent.change(slider, { target: { value: '70' } });

    expect(useDataStore.getState().pipelineConfig.trainTestSplit).toBe(70);
  });

  it('renders SMOTE checkbox, default is unchecked', () => {
    render(<PipelineConfig onApply={onApplyMock} />);

    const smoteCheckbox = screen.getByRole('checkbox');
    expect(smoteCheckbox.checked).toBe(false);
  });

  it('apply button triggers the onApply callback', async () => {
    const user = userEvent.setup();
    render(<PipelineConfig onApply={onApplyMock} />);

    const applyBtn = screen.getByRole('button', { name: /apply pipeline/i });
    await user.click(applyBtn);

    expect(onApplyMock).toHaveBeenCalledTimes(1);
  });

  it('controls are disabled during running state', () => {
    useDataStore.setState({
      pipelineStatus: 'running',
    });

    render(<PipelineConfig onApply={onApplyMock} />);

    const imputationSelect = screen.getByLabelText(/missing value imputation/i);
    const scalingSelect = screen.getByLabelText(/feature scaling/i);
    const slider = screen.getByRole('slider');
    const applyBtn = screen.getByRole('button', { name: /processing/i });

    expect(imputationSelect).toBeDisabled();
    expect(scalingSelect).toBeDisabled();
    expect(slider).toBeDisabled();
    expect(applyBtn).toBeDisabled();
  });
});
