import cytoscape from 'https://cdnjs.cloudflare.com/ajax/libs/cytoscape/3.15.2/cytoscape.esm.min.js';
import Fuse from 'https://cdn.jsdelivr.net/npm/fuse.js@6.4.0/dist/fuse.esm.js';

function graphArea () {
  const div = document.createElement('div');
  div.appendChild(document.createElement('hr'));

  const cy = document.createElement('div');
  cy.classList.add('cytoscape-container');
  cy.style.width = '100%';
  cy.style.height = '80vh';
  cy.style.position = 'relative';
  cy.style.top = '0px';
  cy.style.left = '0px';
  div.appendChild(cy);

  const info = document.createElement('div');
  info.classList.add('info-container');
  div.appendChild(info);
  return div
}

function noteElement (note, currentNote = false) {
  return {
    data: {
      id: note.id,
      title: note.title,
      filename: note.filename,
      label: note.title,
      color: 'white',
      bgColor: currentNote ? 'black' : 'gray'
    }
  }
}

function linkElement (source, target) {
  return {
    data: { id: `${source}-${target}`, source, target, arrow: 'triangle', style: 'solid', color: 'black' }
  }
}

function dfs (graph, src) {
  if (!graph[src]) return []
  const edges = [];
  const done = new Set();
  const stack = [src];
  while (stack.length > 0) {
    const top = stack.pop();
    if (done.has(top)) continue
    const children = graph[top] || [];
    for (const child of children) {
      edges.push([top, child]);
      stack.push(child);
    }
    done.add(top);
  }
  return edges
}

function traverse (query, id) {
  const edges = [];
  for (const { forward, reverse } of Object.values(query.db.data.clusters)) {
    edges.push(...dfs(forward, id));
    edges.push(...dfs(reverse, id).map(([a, b]) => [b, a]));
  }
  return Array.from(new Set(edges.filter(([a, b]) => a !== b)))
}

function * clusterElements (query, tag) {
  const cluster = query.db.data.clusters[tag] || { forward: [] };
  for (const [src, dests] of Object.entries(cluster.forward)) {
    const source = Number(src);
    yield noteElement(query.note(source));
    for (const dest of dests) {
      if (source !== dest) {
        yield noteElement(query.note(dest));
        yield linkElement(source, dest);
      }
    }
  }
}

function * neighborElements (query, note) {
  yield noteElement(note, true);

  for (const backlink of note.backlinks()) {
    yield noteElement(backlink.src);
    yield linkElement(backlink.src.id, note.id);
  }
  for (const link of note.links()) {
    yield noteElement(link.dest);
    yield linkElement(note.id, link.dest.id);
  }
  for (const [src, dest] of traverse(query, note.id)) {
    yield noteElement(query.note(src));
    yield noteElement(query.note(dest));
    yield linkElement(src, dest);
  }
}

function createCytoscape (container, elements) {
  const cy = cytoscape({
    directed: true,
    multigraph: true,
    container: container.querySelector('div.cytoscape-container'),
    elements: elements,
    selectionType: 'additive',
    style: [
      {
        selector: 'node',
        style: {
          label: 'data(label)',
          height: 'label',
          width: 'label',
          padding: '8px',
          shape: 'round-rectangle',
          color: 'data(color)',
          'background-color': 'data(bgColor)',
          'text-halign': 'center',
          'text-valign': 'center',
          'text-wrap': 'wrap',
          'text-max-width': 100
        }
      },
      {
        selector: 'edge',
        style: {
          width: 2,
          'curve-style': 'bezier',
          'line-color': 'data(color)',
          'line-style': 'data(style)'
        }
      },
      {
        selector: 'edge[arrow]',
        style: {
          'target-arrow-color': 'data(color)',
          'target-arrow-shape': 'data(arrow)'
        }
      }
    ]
  });
  cy.layout({
    name: 'breadthfirst',
    spacingFactor: 1.0,
    fit: true,
    directed: true,
    avoidOverlap: true,
    nodeDimensionsIncludeLabels: true
  }).run();
  cy.reset();
  cy.center();

  const infoContainer = container.querySelector('div.info-container');
  const [show, hide] = hoverHandlers(infoContainer);
  cy.on('select', 'node', show);
  cy.on('unselect', 'node', hide);
  return cy
}

function noteInfoDiv () {
  const div = document.createElement('div');
  div.style.bottom = 0;
  div.style.right = 0;
  div.style.padding = '20px';
  div.style.position = 'fixed';
  div.style.maxWidth = '30em';
  div.style.zIndex = 1;
  return div
}

function hoverHandlers (container) {
  const header = document.createElement('header');
  header.innerHTML = '<h3><a href=""></a></h3><p></p>';
  const a = header.querySelector('a');
  const p = header.querySelector('p');

  const infoDiv = noteInfoDiv();
  infoDiv.appendChild(header);
  container.appendChild(infoDiv);

  const show = event => {
    const id = event.target.data('id');
    a.textContent = event.target.data('title');
    a.href = '#' + id;
    p.textContent = event.target.data('filename');
    event.target.data('label', id);
  };
  const hide = event => {
    a.textContent = '';
    p.textContent = '';
    event.target.data('label', event.target.data('title'));
  };
  return [show, hide]
}

function init (query) {
  let container = graphArea();

  function resetGraph () {
    container.remove();
    const id = Number(window.location.hash.slice(1));
    const elements = [];
    if (Number.isInteger(id)) {
      const note = query.note(id);
      if (note != null) {
        elements.push(...neighborElements(query, note));
      }
      if (elements.length < 2) return
    } else {
      elements.push(...clusterElements(query, window.location.hash.slice(1)));
      if (elements.length === 0) return
    }
    container = document.body.appendChild(graphArea());
    createCytoscape(container, elements);
  }

  resetGraph();
  window.addEventListener('hashchange', resetGraph);
}

class Database {
  // Schema
  // {
  //   clusters: {
  //     [tag: string]: {
  //       forward: {
  //         [src: number]: Array<number>
  //       },
  //       reverse: {
  //         [dest: number]: Array<number>
  //       }
  //     }
  //   }
  //   notes: [
  //     {
  //       title: <str>,
  //       filename: <str>,
  //       links: [{ src: <int>, dest: <int>, tag: <str> }],
  //       backlinks: [<link>]
  //     }
  //   ]
  // }

  constructor () {
    this.data = { notes: [], clusters: [] };
  }

  add (record) {
    return record.addTo(this) || record
  }
}

class IntegrityError extends Error {}
class DomainError extends IntegrityError {}
class ReferenceError extends IntegrityError {}

function check (condition, message) {
  if (!condition) throw new DomainError(message)
}

class Note {
  constructor (id, title, filename) {
    check(typeof id === 'number', 'non-number Note.id');
    check(Number.isInteger(id), 'invalid Note.id');
    check(typeof title === 'string', 'invalid Note.title');
    check(typeof filename === 'string', 'invalid Note.filename');
    check(title, 'empty Note.title');
    check(filename, 'missing Note.filename');
    this.id = id;
    this.title = title;
    this.filename = filename;
  }

  addTo (db) {
    // Overwrite existing entry in notes.
    db.data.notes[this.id] = {
      title: this.title,
      filename: this.filename,
      links: [],
      backlinks: []
    };
  }

  equals (note) {
    return this.id === note.id && this.title === note.title && this.filename === note.filename
  }
}

class Link {
  constructor (src, dest, tag) {
    check(src instanceof Note, 'invalid src Note');
    check(dest instanceof Note, 'invalid dest Note');
    check(tag === null || typeof tag === 'string', 'invalid Link.tag');
    this.src = src;
    this.dest = dest;
    this.tag = tag;
  }

  addTo (db) {
    const src = db.data.notes[this.src.id];
    const dest = db.data.notes[this.dest.id];
    if (!src) return new ReferenceError('Link.src')
    if (!dest) return new ReferenceError('Link.dest')

    // Existing entries get overwritten.
    const link = {
      src: this.src,
      dest: this.dest,
      tag: this.tag
    };
    if (this.src.id !== this.dest.id) {
      src.links.push(link);
      dest.backlinks.push(link);
    }
    if (this.tag) {
      const result = db.data.clusters[this.tag] || {
        forward: {},
        reverse: {}
      };
      const forward = result.forward[this.src.id] || [];
      const reverse = result.reverse[this.dest.id] || [];
      forward.push(this.dest.id);
      reverse.push(this.src.id);
      result.forward[this.src.id] = forward;
      result.reverse[this.dest.id] = reverse;
      db.data.clusters[this.tag] = result;
    }
  }
}

class Query {
  constructor (db) {
    this.db = db;
  }

  note (id) {
    const record = this.db.data.notes[id];
    if (!record) return null
    const note = new Note(id, record.title, record.filename);
    note.links = () => this.links(note);
    note.backlinks = () => this.backlinks(note);
    return note
  }

  * links (note) {
    const src = this.db.data.notes[note.id];
    if (src && src.links) {
      yield * src.links;
    }
  }

  * backlinks (note) {
    const dest = this.db.data.notes[note.id];
    if (dest && dest.backlinks) {
      yield * dest.backlinks;
    }
  }
}

var Model = /*#__PURE__*/Object.freeze({
  __proto__: null,
  Database: Database,
  DomainError: DomainError,
  Link: Link,
  Note: Note,
  Query: Query,
  ReferenceError: ReferenceError
});

function createFuse () {
  const options = {
    includeMatches: true,
    ignoreLocation: true,
    keys: ['textContent'],
    threshold: 0.45
  };
  const nodes = document.body.querySelectorAll('section.level1');
  const sections = Array.prototype.filter.call(nodes, function (node) {
    return Number.isInteger(Number(node.id))
  });
  return new Fuse(sections, options)
}

function displayResults (results, container) {
  // Display results in container.
  const div = container;
  div.textContent = '';
  for (const result of results) {
    const p = document.createElement('p');
    const h3 = document.createElement('h3');
    h3.innerHTML = `<a href="#${result.item.id}">${result.item.title}</a>`;
    p.appendChild(h3);

    let count = 3;
    for (const child of result.item.children) {
      const clone = child.cloneNode(true);
      if (count-- <= 0) break
      if (clone.tagName === 'H1' && clone.title === result.item.title) {
        continue
      }
      p.appendChild(clone);
    }

    div.appendChild(p);
    div.appendChild(document.createElement('hr'));
  }
}

function searchBar (fuse, container) {
  // Container will contain search results.
  const input = document.createElement('input');
  input.type = 'text';
  input.placeholder = 'Search notes...';
  input.classList.add('search-bar');
  input.style.width = '100%';
  input.style.background = 'transparent';
  input.style.border = 'none';
  input.style.borderBottomStyle = 'solid';
  input.style.borderWidth = 'thin';

  input.addEventListener('change', function () {
    window.location.hash = '#search';
    const results = fuse.search(input.value);
    displayResults(results, container);
  });
  return input
}

function searchResults () {
  const div = document.createElement('div');
  div.classList.add('search-results');
  return div
}

function searchPage (container) {
  // Container will contain search results.
  const page = document.createElement('section');
  page.id = 'search';
  page.title = 'Search';
  page.classList.add('level1');
  page.appendChild(container);
  return page
}

function searchSpan () {
  const span = document.createElement('span');
  span.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M23.809 21.646l-6.205-6.205c1.167-1.605 1.857-3.579 1.857-5.711 0-5.365-4.365-9.73-9.731-9.73-5.365 0-9.73 4.365-9.73 9.73 0 5.366 4.365 9.73 9.73 9.73 2.034 0 3.923-.627 5.487-1.698l6.238 6.238 2.354-2.354zm-20.955-11.916c0-3.792 3.085-6.877 6.877-6.877s6.877 3.085 6.877 6.877-3.085 6.877-6.877 6.877c-3.793 0-6.877-3.085-6.877-6.877z"/></svg>';
  span.firstChild.style.height = '1em';
  return span
}

function searchForm (container) {
  // Container will contain search results.
  const button = searchSpan();
  const input = searchBar(createFuse(), container);
  input.style.display = 'none';

  button.addEventListener('click', function () {
    button.style.display = 'none';
    input.style.display = '';
    input.focus();
  });

  input.addEventListener('focusout', function () {
    button.style.display = '';
    input.style.display = 'none';
  });

  const div = document.createElement('div');
  div.appendChild(button);
  div.appendChild(input);
  return div
}

function init$1 () {
  const container = searchResults();
  document.body.appendChild(searchPage(container));
  document.body.insertBefore(searchForm(container), document.body.firstChild);
}

function getSectionFromHash (hash) {
  const id = hash.substring(1);
  if (!id) { return null }
  const elem = document.getElementById(id);
  if (elem) {
    return elem.closest('section.level1')
  }
}

function sectionChanger () {
  let _previousHash = window.location.hash;
  return function () {
    const oldSection = getSectionFromHash(_previousHash);
    if (oldSection) {
      oldSection.style.display = 'none';
    }
    _previousHash = window.location.hash;
    const newSection = getSectionFromHash(_previousHash);
    if (newSection) {
      newSection.style.display = '';
      document.title = newSection.title || 'Slipbox';
    } else {
      window.location.hash = '#0';
    }
    window.scrollTo(0, 0);
  }
}

function notFoundSection () {
  const section = document.createElement('section');
  section.id = '0';
  section.classList.add('level1');
  section.style.display = 'none';
  const h1 = document.createElement('h1');
  h1.innerText = 'Note not found';
  section.appendChild(h1);
  return section
}

function init$2 () {
  document.body.appendChild(notFoundSection());
  const changeSection = sectionChanger();
  changeSection();
  window.addEventListener('hashchange', changeSection);
}

window.query = new Query(new Database());

window.Model = Model;

window.initSlipbox = function () {
  const title = document.getElementById('title-block-header');
  if (title) { title.remove(); }
  init$1();
  init$2();
  init(window.query);
};
