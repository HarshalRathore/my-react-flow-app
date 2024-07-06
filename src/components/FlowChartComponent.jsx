import React, { useCallback } from 'react';
import ReactFlow, {
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  addEdge,
} from 'reactflow';
import 'reactflow/dist/style.css';
import data from '../data/data';


const generateNodesAndEdges = (data) => {
  const initialNodes = data.map((item, index) => ({
    id: `${index + 1}`,
    position: { x: 500, y: index * 150 },
    data: { label: `${item.topic}` },
  }));

  const initialEdges = data.slice(1).map((item, index) => ({
    id: `e${index + 1}-${index + 2}`,
    source: `${index + 1}`,
    target: `${index + 2}`,
  }));

  return { initialNodes, initialEdges };
};

const { initialNodes, initialEdges } = generateNodesAndEdges(data);

const FlowChartComponent = ({data}) =>{
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
 
  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      >
        <Controls />
        <MiniMap />
        <Background variant="dots" gap={12} size={1} />
      </ReactFlow>
    </div>
  );
}

export default FlowChartComponent;