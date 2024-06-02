import React, { useState } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';

const App: React.FC = () => {
  const [code, setCode] = useState<string>('');
  const [output, setOutput] = useState<string>('Output goes here');
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);

  const handleTestCode = async () => {
    try {
      setIsRunning(true);
      const response = await axios.post('http://localhost:8000/test-code', { code });
      setOutput(response.data.output + response.data.error);
      setIsRunning(false);
    } catch (error) {
      console.log(error);
      setOutput('Error executing code');
    }
  };

  const handleSubmit = async () => {
    try {
      setIsSubmitting(true);
      const response = await axios.post('http://localhost:8000/submit-code', { code });
      setIsSubmitting(false);
      if (response.data.error) {
        setOutput("Submission failed due to error: \n" + response.data.error);
        return;
      }
      setOutput("Submission succeed: \n" + response.data.output);
    } catch (error) {
      setOutput('Error submitting code');
    }
  };

  return (
    <div className="container flex w-screen max-h-screen min-h-screen">
      <div className='w-1/2 flex flex-col bg-blue-950'>
        <div className="flex justify-between items-center mb-0" style={{ minHeight: "50px", maxHeight: "50px" }}>
          <h1 className="text-2xl font-bold p-2 text-white">Python Interpreter</h1>
          <div>
            <button onClick={handleTestCode} className="bg-blue-500 px-4 py-2 rounded text-white mx-4">Run</button>
            <button onClick={handleSubmit} className="bg-green-500 px-4 py-2 rounded text-white mr-8">Save</button>
          </div>
        </div>
        <Editor
          theme='vs-dark'
          height="100%"
          width="50vw"
          defaultLanguage="python"
          defaultValue="# Write your Python code here"
          onChange={(value) => setCode(value || '')}
        />
      </div>
      <div className="flex flex-col bg-blue w-full" style={{ minWidth: "50vw" }}>
        <h1 className="text-xl font-bold my-0 flex items-center p-2 bg-blue-950 text-white" style={{ minHeight: "50px", maxHeight: "50px"}}>Output</h1>
        <pre className="flex-1 min-w-full overflow-auto p-4 text-white" style={{ backgroundColor: "#1e1e1e" }}>
          {isRunning ? "Running ..." : isSubmitting ? "Submitting ..." : output}</pre>
      </div>
    </div>

  );
};

export default App;
