interface ControlsProps {
  numOutputs: number;
  onNumOutputsChange: (n: number) => void;
  onSubmit: () => void;
  submitDisabled: boolean;
  isLoading: boolean;
}

export function Controls({ numOutputs, onNumOutputsChange, onSubmit, submitDisabled, isLoading }: ControlsProps) {
  return (
    <div className="mv-controls-row">
      <div className="mv-slider-group">
        <label className="mv-slider-label">Recommendations</label>
        <input
          className="mv-slider"
          type="range"
          min={1}
          max={10}
          value={numOutputs}
          onChange={(e) => onNumOutputsChange(Number(e.target.value))}
        />
        <span className="mv-slider-value">{numOutputs}</span>
      </div>
      <button className="mv-submit-btn" onClick={onSubmit} disabled={submitDisabled}>
        {isLoading ? "Calculating…" : "Generate recommendations"}
      </button>
    </div>
  );
}
